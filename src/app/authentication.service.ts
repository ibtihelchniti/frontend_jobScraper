import { Injectable, PLATFORM_ID, Inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs'; 
import { delay } from 'rxjs/operators';
import { tap } from 'rxjs/operators'; 
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private apiUrl = "http://127.0.0.1:5000";
  private isAuthenticated: boolean = false;
  private username: string = '';

  constructor(
    private http: HttpClient,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {
    // Check if the platform is the browser before accessing localStorage
    if (isPlatformBrowser(this.platformId)) {
      this.isAuthenticated = !!localStorage.getItem('isAuthenticated');
      this.username = localStorage.getItem('username') || '';
    }
  }

  // Méthode pour vérifier si l'utilisateur est authentifié
  isAuthenticatedUser(): Observable<boolean> {
    // Check if localStorage is available before accessing it
    if (isPlatformBrowser(this.platformId) && localStorage) {
      return of(this.isAuthenticated || !!localStorage.getItem('isAuthenticated')).pipe(
        delay(0) // Utiliser delay pour rendre la réponse asynchrone
      );
    } else {
      // Return false if localStorage is not available
      return of(false);
    }
  }
  

  login(username: string, password: string): Observable<any> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    // Effectuer la requête HTTP
    return this.http.post(`${this.apiUrl}/login`, formData)
      .pipe(
        // Utiliser pipe pour gérer la réponse
        tap((response: any) => {
          if (response && response.message === 'Authentification réussie') {
            this.isAuthenticated = true; // Mettre à jour l'état de l'authentification
            this.username = username; // Mettre à jour le nom d'utilisateur
            this.router.navigate(['/sites']); // Rediriger vers la liste des sites après l'authentification réussie
            this.username = username;
            // Stocker l'état d'authentification et le nom d'utilisateur dans le localStorage
            localStorage.setItem('isAuthenticated', 'true');
            localStorage.setItem('username', username);
            this.router.navigate(['/sites']);
          }
        })
      );
  }

  logout(): void {
    this.http.post(`${this.apiUrl}/logout`, {}).subscribe(
      () => {
        this.isAuthenticated = false;
        this.router.navigate(['/login']);
      },
      (error: HttpErrorResponse) => { 
        console.error('Erreur lors de la déconnexion', error);
        if (error.status === 401) {
          alert('Erreur lors de la déconnexion : Vous n\'êtes pas authentifié.');
        } else {
          alert('Erreur lors de la déconnexion : ' + error.message);
        }
      }
    );
    // Mettre à jour la variable isAuthenticated
    this.isAuthenticated = false;
    // Supprimer les informations d'authentification du localStorage lors de la déconnexion
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('username');
  }




  getUsername(): string {
    return this.username;
  }
}
