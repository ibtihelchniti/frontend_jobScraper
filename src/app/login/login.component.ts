import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthenticationService } from '../authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  username: string = '';
  password: string = '';
  isAuthenticated: boolean = false;
  returnUrl: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthenticationService
  ) {}

  ngOnInit(): void {
    // Récupérer le paramètre de redirection après un rafraîchissement
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/sites';
  }

  login(): void {
    this.authService.login(this.username, this.password).subscribe(
      () => {
        this.router.navigateByUrl(this.returnUrl); // Rediriger vers l'URL précédente après l'authentification
      },
      (error) => {
        console.error('Erreur de login', error);
        alert('Erreur de login : ' + error.message);
      }
    );
  }
  logout(): void {
    this.authService.logout(); // Appeler la méthode de déconnexion du service d'authentification
    this.router.navigate(['/login']); // Rediriger vers la page de connexion
  }

  // Méthode pour récupérer le nom d'utilisateur actuellement connecté
  getUsername(): string {
    return this.authService.getUsername();
  }
}
