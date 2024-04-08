import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ScrapingService } from '../scraping.service';


// Interface pour définir la structure des sites
interface Site {
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
      name: 'Free Work En', 
      url: 'https://www.free-work.com/en-gb/tech-it/jobs', 
      isScraping: false, 
      isExportingCSV: false,
      scrapingCompleted: false,
      lastScrapingDate: '', 
      scrapingStatus: '' 
    },
    
    { 
      name: 'Free Work Fr', 
      url: 'https://www.free-work.com/fr/tech-it/jobs', 
      isScraping: false, 
      isExportingCSV: false,
      scrapingCompleted: false,
      lastScrapingDate: '', 
      scrapingStatus: '' 
    },

    { 
      name: 'Choose Your Boss', 
      url: 'https://www.chooseyourboss.com/offres/emploi-it', 
      isScraping: false, 
      isExportingCSV: false,
      scrapingCompleted: false,
      lastScrapingDate: '', 
      scrapingStatus: '' 
    },
  ];

  constructor(private router: Router, private scrapingService: ScrapingService) { }

  ngOnInit(): void {
    this.getScrapingHistory(); 
  }

  
  // Fonction pour récupérer l'historique de scraping depuis le backend
  getScrapingHistory(): void {
    this.scrapingService.getScrapingHistory().subscribe(
        (history: Object) => {  
            const historyArray = Object.values(history); // Convertir l'objet d'historique en tableau
            historyArray.forEach((historyItem: any) => { // Parcourir chaque élément d'historique
                const index = this.sites.findIndex(site => site.url === historyItem.site_url); // Trouver l'index du site correspondant dans le tableau
                if (index !== -1) {
                  // Mettre à jour les informations de scraping du site
                    this.sites[index].lastScrapingDate = historyItem.lastScrapingDate;
                    this.sites[index].scrapingStatus = historyItem.scrapingStatus;
                }
            });
        },
        (error) => {
            console.error('Erreur lors de la récupération de l\'historique de scraping', error);
            alert ('Erreur lors de la récupération de l\'historique de scraping. Détails : ' + error.message);
        }
    );
  }

  
  // Fonction pour lancer le scraping d'un site
  toggleScraping(site: Site): void {
    // Appeler la fonction de scraping appropriée en fonction du nom du site
    if (site.name === 'Free Work En') {
      this.toggleScrapingEn(site);
    } else if (site.name === 'Free Work Fr') {
      this.toggleScrapingFr(site);
    } else if (site.name === 'Choose Your Boss') {
      this.toggleScrapingCh(site);
    }
  }

  
  // Fonction pour lancer le scraping du site Free Work En
  toggleScrapingEn(site: Site): void {
    site.isScraping = true; // Mettre l'indicateur de scraping à vrai
    this.scrapingService.scrapeJobsEn(site.url).subscribe( // Appeler le service de scraping pour le site Free Work En
      (response) => { // En cas de succès du scraping
        console.log('Scraping réussi', response);
        alert('Le scraping pour le site' + site.name + 'a été réussi.');

        // Mettre à jour les informations du site
        site.isScraping = false;
        site.scrapingCompleted = true;
        site.lastScrapingDate = new Date().toLocaleString();
        site.scrapingStatus = 'Réussi';

        // Réinitialiser l'état des boutons après un court délai
        setTimeout(() => {
          site.isScraping = false;
          site.scrapingCompleted = false;
          site.scrapingStatus = '';
        }, 2000); // 2000 millisecondes = 2 secondes

      },

      (error) => { // En cas d'échec du scraping
        console.error('Erreur lors du scraping', error);
        alert('Erreur lors du scraping pour le site' + site.name + '. Détails : ' + error.message);

        // Mettre à jour les informations du site
        site.isScraping = false;
        site.lastScrapingDate = new Date().toLocaleString();
        site.scrapingStatus = 'Echoué';

        setTimeout(() => {
          site.isScraping= false;
          site.scrapingCompleted = false;
          site.scrapingStatus = '';
        }, 2000); 
      }
    );
  }

  
  // Fonction pour lancer ou arrêter le scraping du site Free Work Fr
  toggleScrapingFr(site: Site): void {
    site.isScraping = true; // Mettre l'indicateur de scraping à vrai
    this.scrapingService.scrapeJobsFr(site.url).subscribe( // Appeler le service de scraping pour le site Free Work Fr
      (response) => { // En cas de succès du scraping
        console.log('Scraping réussi', response);
        alert('Le scraping pour le site' + site.name + 'a été réussi.');

        // Mettre à jour les informations du site
        site.isScraping = false;
        site.scrapingCompleted = true;
        site.lastScrapingDate = new Date().toLocaleString();
        site.scrapingStatus = 'Réussi';

        // Réinitialiser l'état des boutons après un court délai
        setTimeout(() => {
          site.isScraping= false;
          site.scrapingCompleted = false;
          site.scrapingStatus = '';
        }, 2000); // 2000 millisecondes = 2 secondes
      },
      (error) => { // En cas d'échec du scraping
        console.error('Erreur lors du scraping', error);
        alert('Erreur lors du scraping pour le site' + site.name + '. Détails : ' + error.message);

        site.isScraping = false;
        site.lastScrapingDate = new Date().toLocaleString();
        site.scrapingStatus = 'Echoué';

        setTimeout(() => {
          site.isScraping= false;
          site.scrapingCompleted = false;
          site.scrapingStatus = '';
        }, 2000); 
      }
    );
  }

  
  // Fonction pour lancer ou arrêter le scraping du site Choose Your Boss
  toggleScrapingCh(site: Site): void {
    site.isScraping = true; // Mettre l'indicateur de scraping à vrai
    this.scrapingService.scrapeJobsCh(site.url).subscribe( // Appeler le service de scraping pour le site Choose Your Boss
      (response) => { // En cas de succès du scraping
        console.log('Scraping réussi', response);
        alert('Le scraping pour le site' + site.name + 'a été réussi.');

        // Mettre à jour les informations du site
        site.isScraping = false;
        site.scrapingCompleted = true;
        site.lastScrapingDate = new Date().toLocaleString();
        site.scrapingStatus = 'Réussi';

        // Réinitialiser l'état des boutons après un court délai
        setTimeout(() => {
          site.isScraping= false;
          site.scrapingCompleted = false;
          site.scrapingStatus = '';
        }, 2000); // 2000 millisecondes = 2 secondes
      },
      (error) => { // En cas d'échec du scraping
        console.error('Erreur lors du scraping', error);
        alert('Erreur lors du scraping pour le site' + site.name + '. Détails : ' + error.message);

        site.isScraping = false;
        site.lastScrapingDate = new Date().toLocaleString();
        site.scrapingStatus = 'Echoué';

        setTimeout(() => {
          site.isScraping= false;
          site.scrapingCompleted = false;
          site.scrapingStatus = '';
        }, 2000); 
      }
    );
  }


  // Fonction pour exporter les données en CSV
  exportCSV(site: Site): void {
    // Mettre les indicateurs de scraping et d'exportation à vrai
    site.isExportingCSV = true;  
    site.isScraping = true;

    this.scrapingService.exportToCSV(site.name).subscribe(
        (response: Blob) => {
            console.log('Réponse de l\'exportation CSV', response);
            // Créer un objet URL pour le Blob et ouvrir le lien dans une nouvelle fenêtre
            const blobUrl = URL.createObjectURL(response);
            window.open(blobUrl, '_blank');
        },
        (error) => {
            console.error('Erreur lors de l\'exportation CSV', error);
            alert('Une erreur est survenue lors de l\'exportation en CSV pour le site ' + site.name + '. Détails : ' + error.message);
        },
        () => {
          site.isExportingCSV = false;  
          site.isScraping = false;  
        }
    );
  }

  // méthode pour ouvrir la page de configuration du site
  openConfig(site: Site): void {
    // Redirigez l'utilisateur vers la page de configuration avec le nom du site
    this.router.navigate(['/config', site.name.replace(/\s/g, '-')]);
     
  }





}