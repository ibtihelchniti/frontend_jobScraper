from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import hashlib
from .base_scraper import BaseScraper
from db.database import insert_job_offer_into_db


#Définition de la classe qui hérite de base scraper
class ChooseYourBoss(BaseScraper):
    def __init__(self, driver):
        super().__init__('https://www.chooseyourboss.com/offres/emploi-it') # URL du site à scraper
        self.driver = driver 
        self.scraped_data = [] # Liste pour stocker les données scrapées

    
    # Méthode pour scraper les offres d'emploi
    def scrape_jobs(self):
        try:
            self.driver.get(self.url) # Chargement de l'URL
            while True:
                self._wait_for_job_elements() # Attendre que les éléments d'offre d'emploi soient présents
                self._scrape_current_page() # Scraper la page actuelle
                if not self._go_to_next_page(): # Passer à la page suivante
                    print("Fin des pages d'offre d'emploi.")
                    break
        except Exception as e:
            print(f"Erreur lors du scraping : {e}")
        finally:
            self.driver.quit()

        return self.scraped_data  # Renvoyer les données extraites

    
    # Méthode pour attendre que les éléments d'offre d'emploi soient chargés
    def _wait_for_job_elements(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.col-md-8.col-xs-12 > div.card.offer')))

    
    # Méthode pour cliquer sur le bouton "Voir l'offre d'emploi"
    def _click_view_job_button(self, job_element):
        try:
            job_url = job_element.find_element(By.CSS_SELECTOR, '.offer__title.top a').get_attribute('href') # Récupérer l'URL de l'offre
            self.driver.execute_script(f"window.open('{job_url}','_blank');") # Ouvrir l'URL dans une nouvelle fenêtre
            self.driver.switch_to.window(self.driver.window_handles[-1]) # Passer à la nouvelle fenêtre
            time.sleep(3) # Attendre le chargement de la page 
        except Exception as e:
            print(f"Impossible d'ouvrir l'URL de l'offre d'emploi : {e}")

    
    # Méthode pour scraper les détails de l'offre sur la page actuelle
    def _scrape_current_page(self):
        while True:
            job_offers = self.driver.find_elements(By.CSS_SELECTOR, 'div.col-md-8.col-xs-12 > div.card.offer ')
            for job in job_offers:
                try:
                    self._click_view_job_button(job)  # Ouvre la page d'offre d'emploi
                    
                    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ' div.well > div'))) # Attendre que la page de détails de l'offre soit chargée
                    
                    # Scraper les détails de l'offre
                    job_details = self.driver.find_element(By.CSS_SELECTOR, 'div.container-fluid')
                    title = self._get_element_text(job_details, 'div.headline > h1')
                    company = self._get_element_text(job_details, 'div.headline > div > a')
                    job_type = self._get_element_text(job_details, 'div.details > ul > li:nth-child(1)')
                    salary = self._get_element_text(job_details, 'div.details > ul > li:nth-child(2)')
                    experience = self._get_element_text(job_details, 'div.details > ul > li:nth-child(3)')
                    location = self._get_element_text(job_details, 'div.details > ul > li:nth-child(4)')
                    unique_id = hashlib.md5((title + company).encode('utf-8')).hexdigest()

                    # Scraper la description de l'offre tout en conservant la mise en forme
                    job_description = self.driver.find_element(By.CSS_SELECTOR, 'div.col-xs-12.col-md-8')
                    description_elements = job_description.find_elements(By.CSS_SELECTOR, 'div.well > div')
                    description = '\n\n\n'.join([element.get_attribute('innerHTML') for element in description_elements])

                    # Scraper l'URL du logo de l'entreprise si l'élément est présent
                    logo_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.thumbnail.thumbnail-xl.thumbnail--light > img.img-responsive')
                    if logo_elements:
                        logo_url = logo_elements[0].get_attribute('src')
                    else:
                        logo_url = None

                    # Imprimer les détails de l'offre
                    print(f'Titre: {title}\nEntreprise: {company}\nLocalisation: {location}\nType: {job_type}\nLogo: {logo_url}\nSalaire: {salary}\nExpérience nécessaire: {experience}\nDescription: {description}\n{"-"*20}')

                    # Insérer les détails de l'offre dans la base de données
                    insert_job_offer_into_db(unique_id, title, company, location, job_type, salary, experience, description, logo_url)

                    self.scraped_data.append({
                        "unique_id": unique_id,
                        "title": title,
                        "company": company,
                        "location": location,
                        "job_type": job_type,
                        "salary": salary,
                        "experience": experience,
                        "description": description,
                        "logo_url": logo_url,
                    })

                except Exception as e:
                    print(f"Erreur lors du scraping de cette offre : {e}")
                    
                finally:
                    # Fermer la fenêtre actuelle et revenir à la fenêtre précédente
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    time.sleep(3)  # Attendre que la page se recharge

            if not self._go_to_next_page():
                break

    
    # Méthode pour récupérer le texte d'un élément
    def _go_to_next_page(self):
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.pagination li:last-child a[rel="next"]'))
            )
            next_button.click()
            time.sleep(3)
            return True
        except Exception as e:
            print(f"Impossible de passer à la page suivante : {e}")
            return False



    # Méthode pour passer à la page suivante
    def _get_element_text(self, parent_element, css_selector, default="-"):
        try:
            return parent_element.find_element(By.CSS_SELECTOR, css_selector).text.strip()
        except:
            return default


    