import { Injectable } from '@angular/core';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ScrapingService {

  private apiUrl = "http://127.0.0.1:5000";

  constructor(private http: HttpClient) { }

  getSiteDetailsById(siteId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/site-details/${siteId}`);
  }


  scrapeJobsEn(url: string) {
    return this.http.get(`${this.apiUrl}/scrape-en?url=${encodeURIComponent(url)}`);
  }

  scrapeJobsFr(url: string) {
    return this.http.get(`${this.apiUrl}/scrape-fr?url=${encodeURIComponent(url)}`);
  }

  scrapeJobsCh(url: string) {
    return this.http.get(`${this.apiUrl}/scrape-ch?url=${encodeURIComponent(url)}`);
  }
  

  getScrapingHistory(): Observable<any[]> { 
    return this.http.get<any[]>(`${this.apiUrl}/scraping-history`); 
  }


  exportToCSV(siteId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/export-csv?site_id=${encodeURIComponent(siteId)}`, { responseType: 'blob' });
  }
  



  getSiteDetails(siteName: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/site-details/${siteName}`);
  }


  updateSiteDetails(siteId: number, newName: string, newUrl: string): Observable<any> {
    return this.http.put(`${this.apiUrl}/site-details/${siteId}`, { name: newName, url: newUrl });
  }
  
}
