import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ScrapingService } from '../scraping.service';
import { Router } from '@angular/router'; 

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent implements OnInit {

  siteId: number = 0;
  siteName: string = '';
  siteUrl: string = '';

  constructor(private route: ActivatedRoute, private scrapingService: ScrapingService, private router: Router) { }


  ngOnInit(): void {
    this.siteId = +this.route.snapshot.params['siteId']; // Récupération de l'identifiant du site à partir des paramètres d'URL
    this.fetchSiteDetails(this.siteId); // Appel de la fonction pour récupérer les détails du site
  }

  // Fonction pour récupérer les détails du site à partir de son identifiant
  fetchSiteDetails(siteId: number): void {
    this.scrapingService.getSiteDetailsById(siteId).subscribe(
      (siteDetails: any) => {
        this.siteId = siteId; // Récupérer l'identifiant du site
        this.siteName = siteDetails.site_name; // Récupérer le nom du site à partir de la base de données
        this.siteUrl = siteDetails.site_url; // Récupérer l'URL du site à partir de la base de données
      },
      (error: any) => {
        console.error('Error fetching site details:', error);
      }
    );
  }

  // Fonction pour mettre à jour les détails du site
  updateSiteDetails(): void {
    // Mettre à jour les détails du site avec le nom et l'URL
    this.scrapingService.updateSiteDetails(this.siteId, this.siteName, this.siteUrl).subscribe(
      (response: any) => {
        console.log('Détails du site mis à jour avec succès :', response);
        // Rediriger vers la liste des sites après la mise à jour réussie
        this.router.navigate(['/site-list']);
      },
      (error: any) => {
        console.error('Erreur lors de la mise à jour des détails du site :', error);
      }
    );
}

}
