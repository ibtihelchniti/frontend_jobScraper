class BaseScraper:
    def __init__(self, url):
        self.url = url

    def scrape_jobs(self):
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes.")

