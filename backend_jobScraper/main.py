from backend_jobScraper.scrapers.free_work_eng import FreeWorkEn
from backend_jobScraper.scrapers.free_work_fr import FreeWorkFr 

def main():
    from utils.webdriver import init_webdriver
    driver = init_webdriver()
    
    # Scraping du site "free work fr"
    scraper_fr = FreeWorkFr(driver)
    scraper_fr.scrape_jobs()
    
    # Scraping du site "free work en"
    scraper_en = FreeWorkEn(driver)
    scraper_en.scrape_jobs()

if __name__ == "__main__":
    main()
