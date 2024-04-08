import { Injectable } from '@angular/core';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ScrapingService {

  private apiUrl = "http://127.0.0.1:5000";

  constructor(private http: HttpClient) { }

  scrapeJobsEn(url: string) {
    return this.http.get(`${this.apiUrl}/scrape-en?url=${encodeURIComponent(url)}`);
  }

  scrapeJobsFr(url: string) {
    return this.http.get(`${this.apiUrl}/scrape-fr?url=${encodeURIComponent(url)}`);
  }

  scrapeJobsCh(url: string) {
    return this.http.get(`${this.apiUrl}/scrape-ch?url=${encodeURIComponent(url)}`);
  }

  getScrapingHistory() {
    return this.http.get(`${this.apiUrl}/scraping-history`);
  }


  exportToCSV(site: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/export-csv?site=${encodeURIComponent(site)}`, { responseType: 'blob' });
  }


  getSiteDetails(siteName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/site-details/${siteName}`);
  }

  updateSiteDetails(siteName: string, siteUrl: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/site-details/${siteName}`, { url: siteUrl });
  }


}
