from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import hashlib
from .base_scraper import BaseScraper
from db.database import insert_job_offer_into_db

class FreeWorkEn(BaseScraper):
    def __init__(self, driver):
        super().__init__('https://www.free-work.com/en-gb/tech-it/jobs') 
        self.driver = driver 
        self.scraped_data = []

    def scrape_jobs(self):
        try:
            self.driver.get(self.url)
            while True:
                self._wait_for_job_elements()
                self._scrape_current_page()
                if not self._go_to_next_page():
                    print("Fin des pages d'offre d'emploi.")
                    break
        except Exception as e:
            print(f"Erreur lors du scraping : {e}")
        finally:
            self.driver.quit()
        
        return self.scraped_data

    def _wait_for_job_elements(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.px-4.pb-4.flex.flex-col.h-full'))
        )


    def _click_view_job_button(self, job_element):
        try:
            # Récupérer l'URL de l'offre d'emploi
            job_url = job_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            # Ouvrir l'URL dans une nouvelle fenêtre
            self.driver.execute_script(f"window.open('{job_url}','_blank');")
            # Passer à la nouvelle fenêtre
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)  # Attendre que la page des détails de l'offre soit chargée
        except Exception as e:
            print(f"Impossible d'ouvrir l'URL de l'offre d'emploi : {e}")

    def _scrape_current_page(self):
        job_offers = self.driver.find_elements(By.CSS_SELECTOR, 'div.px-4.pb-4.flex.flex-col.h-full')
        for job in job_offers:
            try:
                location = self._get_element_text(job, 'span.block.flex-1')
                self._click_view_job_button(job)  # Ouvre la page d'offre d'emploi dans une nouvelle fenêtre
                
                # Attendre que la page de détails de l'offre soit chargée
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.html-renderer.prose-content')))
                
                # Scraper les détails de l'offre
                job_details = self.driver.find_element(By.CSS_SELECTOR, 'div.w-full.mx-auto.px-4.md\:px-8.py-4.bg-dot.flex-1')
                title = self._get_element_text(job_details, 'p.text-xl.font-semibold')
                company = self._get_element_text(job_details, 'p.font-semibold')
                job_type = self._get_element_text(job_details, 'div.tags div.truncate')
                unique_id = hashlib.md5((title + company).encode('utf-8')).hexdigest()
                
                description_elements = job_details.find_elements(By.CSS_SELECTOR, 'div.html-renderer.prose-content p')
                description = '\n\n\n'.join([element.get_attribute('innerHTML') for element in description_elements])

                # Scraper l'URL du logo de l'offre si l'élément est présent
                logo_elements = job_details.find_elements(By.CSS_SELECTOR, 'div.flex > a > img')
                if logo_elements:
                    logo_url = logo_elements[0].get_attribute('src')
                else:
                    logo_url = None


                salary = None
                experience = None
                list_items = job_details.find_elements(By.CSS_SELECTOR, 'div.grid > div.flex.items-center.py-1')

                for item in list_items:
                    text = self._get_element_text(item, 'span.text-sm.line-clamp-2')  
                    if '£' in text or '⁄day' in text:  
                        salary = text
                    elif 'years' in text or 'experience' in text: 
                        experience = text

                # Imprimer les détails de l'offre
                print(f'Titre: {title}\nEntreprise: {company}\nLocalisation: {location}\nType: {job_type}\nLogo: {logo_url}\nSalaire: {salary}\nExpérience nécessaire: {experience}\nDescription: {description}\n{"-"*20}')

                # Insérer les détails de l'offre dans la base de données
                insert_job_offer_into_db(unique_id, title, company, logo_url, location, job_type, salary, experience, description)

                self.scraped_data.append({
                        "unique_id": unique_id,
                        "title": title,
                        "company": company,
                        "logo_url": logo_url,
                        "location": location,
                        "job_type": job_type,
                        "salary": salary,
                        "experience": experience,
                        "description": description,
                    })

            except Exception as e:
                print(f"Erreur lors du scraping de cette offre : {e}")
                
            finally:
                # Fermer la fenêtre actuelle et revenir à la fenêtre précédente
                if len(self.driver.window_handles) > 1:
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                time.sleep(3)  # Attendre que la page se recharge


    def _get_element_text(self, parent_element, css_selector, default="-"):
        try:
            return parent_element.find_element(By.CSS_SELECTOR, css_selector).text.strip()
        except:
            return default

    def _go_to_next_page(self):
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-page][href*="page="]:not([disabled])'))
            )
            next_button.click()
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Impossible de passer à la page suivante : {e}")
            return False

