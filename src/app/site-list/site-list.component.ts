import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ScrapingService } from '../scraping.service';
import { Observable } from 'rxjs';
import { DatePipe } from '@angular/common';


// Interface pour définir la structure des sites
interface Site {
  id: number;
  name: string;
  url: string;
  isScraping: boolean; // Indique si le scraping est en cours
  isExportingCSV: boolean; // Indique si l'exportation en CSV est en cours
  scrapingCompleted: boolean; // Indique si le scraping est terminé
  lastScrapingDate: string; // Date du dernier scraping
  scrapingStatus: string; // Statut du scraping (Réussi ou Échoué)
}

@Component({
  selector: 'app-site-list',
  templateUrl: './site-list.component.html',
  styleUrls: ['./site-list.component.css']
})

export class SiteListComponent implements OnInit {
  apiUrl = "http://127.0.0.1:5000"; // URL de l'API

  sites: Site[] = [
    // Liste des sites à scraper
    { 
      id: 1,
      name: '', 
      url: '', 
      isScraping: false, 
      isExportingCSV: false,
      scrapingCompleted: false,
      lastScrapingDate: '', 
      scrapingStatus: '' 
    },
    
    { 
      id: 2,
      name: '', 
      url: '', 
      isScraping: false, 
      isExportingCSV: false,
      scrapingCompleted: false,
      lastScrapingDate: '', 
      scrapingStatus: '' 
    },

    { 
      id: 3,
      name: '', 
      url: '', 
      isScraping: false, 
      isExportingCSV: false,
      scrapingCompleted: false,
      lastScrapingDate: '', 
      scrapingStatus: '' 
    },
  ];

  constructor(private router: Router, private scrapingService: ScrapingService, private datePipe: DatePipe) { } // Injecter le service de routage et le service de scraping dans le composant

  ngOnInit(): void {
    this.sites.forEach(site => {
        this.getSiteDetailsById(site.id); // Appeler la fonction pour récupérer les détails des sites au chargement du composant
    });
    this.getScrapingHistory(); // Appeler la fonction pour récupérer l'historique de scraping au chargement du composant
  }

  
  // Fonction pour récupérer les détails d'un site par son ID depuis le backend
  getSiteDetailsById(siteId: number): void {
    this.scrapingService.getSiteDetailsById(siteId).subscribe(
        (data: any) => {
            const site = this.sites.find(s => s.id === siteId);
            if (site) {
                site.name = data.site_name;
                site.url = data.site_url;
                site.lastScrapingDate = data.lastScrapingDate; 
                site.scrapingStatus = data.scrapingStatus;
            }
        },
        (error) => {
            console.error('Erreur lors de la récupération des détails des sites', error);
            alert('Erreur lors de la récupération des détails des sites. Détails : ' + error.message);
        }
    );
  } 


  
  // Fonction pour lancer le scraping d'un site
  toggleScraping(site: Site): void {
    this.scrapeJobs(site.id); // Appeler la fonction pour scraper les offres d'emploi d'un site
  }

  // Fonction pour scraper les offres d'emploi d'un site
  scrapeJobs(siteId: number): void {
    const site = this.sites.find(site => site.id === siteId);
    if (!site) return; // Site non trouvé

    site.isScraping = true; // Définir l'indicateur de scraping à true

    let scrapeObservable: Observable<any>;

    switch (siteId) {
      // Cas pour Free Work En
      case 1:
        scrapeObservable = this.scrapingService.scrapeJobsEn(site.url);
        break;
      // Cas pour Free Work Fr
      case 2:
        scrapeObservable = this.scrapingService.scrapeJobsFr(site.url);
        break; 
      // Cas pour Choose Your Boss
      case 3:
        scrapeObservable = this.scrapingService.scrapeJobsCh(site.url);
        break;
      default:
        console.error('Invalid site ID for scraping');
        return;
    }

    scrapeObservable.subscribe(
      (response) => {
        console.log('Scraping successful', response);
        alert('Scraping for ' + site.name + ' was successful.');
  
        // Mettre à jour les informations du site après un scraping réussi
        this.updateSiteScrapingInfo(site, true);
      },
      (error) => {
        console.error('Scraping error', error);
        alert('Error scraping for ' + site.name + '. Details: ' + error.message);
  
        // Mettre à jour les informations du site après un échec de scraping
        this.updateSiteScrapingInfo(site, false);
      }
    );
  }
  
  updateSiteScrapingInfo(site: Site, success: boolean): void {
    site.isScraping = false;
    site.scrapingCompleted = true;
    site.lastScrapingDate = new Date().toLocaleString(); // Mettre à jour avec la date réelle
    site.scrapingStatus = success ? 'Success' : 'Failed';
  
    // Réinitialiser les états des boutons après un court délai
    setTimeout(() => {
      site.isScraping = false;
      site.scrapingCompleted = false;
      site.scrapingStatus = '';
    }, 2000);
  }
  
  

  // Dans la méthode getScrapingHistory, mettez à jour le traitement des dates
  getScrapingHistory(): void {
    this.scrapingService.getScrapingHistory().subscribe(
      (history: any[]) => {
        this.sites.forEach(site => {
          const historyForSite = history.find(item => item.site_url === site.url);
          if (historyForSite) {
            site.lastScrapingDate = historyForSite.lastScrapingDate;
            site.scrapingStatus = historyForSite.scrapingStatus;
          }
        });
      },
      (error) => {
        console.error('Erreur lors de la récupération de l\'historique de scraping', error);
        alert('Erreur lors de la récupération de l\'historique de scraping. Détails : ' + error.message);
      }
    );
  }
  


  // Fonction pour exporter les données en CSV
  exportCSV(site: Site): void {
    // Mettre les indicateurs de scraping et d'exportation à vrai
    site.isExportingCSV = true;
    site.isScraping = true;
  
    this.scrapingService.exportToCSV(site.id.toString()).subscribe(
      (response: Blob) => {
        const blob = new Blob([response], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const anchor = document.createElement('a');
        const csvFileName = `${site.name.replace(/[^a-z0-9]/gi, '_')}_${new Date().toISOString()}.csv`;
        anchor.href = url;
        anchor.download = csvFileName; // Utiliser le nom spécifique du fichier CSV
        anchor.click();
  
        // Réinitialiser les indicateurs après le téléchargement
        site.isExportingCSV = false;
        site.isScraping = false;
      },
      (error) => {
        console.error('Erreur lors de l\'exportation CSV', error);
        alert('Une erreur est survenue lors de l\'exportation en CSV pour le site ' + site.name + '. Détails : ' + error.message);
  
        // Réinitialiser les indicateurs en cas d'erreur
        site.isExportingCSV = false;
        site.isScraping = false;
      }
    );
  }
  

  // méthode pour ouvrir la page de configuration du site
  openConfig(site: Site): void {
    this.router.navigate(['/config', site.id]);  
  }

}