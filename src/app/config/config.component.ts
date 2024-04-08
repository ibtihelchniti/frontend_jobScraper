import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ScrapingService } from '../scraping.service';

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.css']
})
export class ConfigComponent implements OnInit {

  siteName: string = '';
  siteUrl: string = '';

  constructor(private route: ActivatedRoute, private scrapingService: ScrapingService) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.siteName = params['siteName'];
      // Fetch the site details using the site name from the backend
      this.fetchSiteDetails(this.siteName);
    });
  }

  fetchSiteDetails(siteName: string): void {
    this.scrapingService.getSiteDetails(siteName).subscribe(
      (siteDetails: any) => {
        this.siteUrl = siteDetails.url; // Update site URL from fetched details
      },
      (error: any) => {
        console.error('Error fetching site details:', error);
        // Handle error or display a message to the user
      }
    );
  }

  updateSiteDetails(): void {
    this.scrapingService.updateSiteDetails(this.siteName, this.siteUrl).subscribe(
      (response: any) => {
        console.log('Site details updated successfully:', response);
        // Handle success, e.g., display a success message
      },
      (error: any) => {
        console.error('Error updating site details:', error);
        // Handle error or display a message to the user
      }
    );
  }

}
