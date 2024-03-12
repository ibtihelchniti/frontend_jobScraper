from backend_jobScraper.scrapers.free_work_en import FreeWorkEn
from backend_jobScraper.scrapers.free_work_fr import FreeWorkFr 
from backend_jobScraper.scrapers.choose_your_boss import ChooseYourBoss
from utils.webdriver import init_webdriver

def main():
    
    driver = init_webdriver()

    # Scraping du site "free work en"
    scraper_en = FreeWorkEn(driver)
    scraper_en.scrape_jobs()
    
    # Scraping du site "free work fr"
    scraper_fr = FreeWorkFr(driver)
    scraper_fr.scrape_jobs()
    
    # Scraping du site "choose your boss"
    scraper_ch = ChooseYourBoss(driver)
    scraper_ch.scrape_jobs()

if __name__ == "__main__":
    main()
