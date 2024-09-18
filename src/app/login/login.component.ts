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
  errorMessage: string = '';
  passwordVisible: boolean = false; // Gérer la visibilité du mot de passe

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private authService: AuthenticationService
  ) {}

  ngOnInit(): void {
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/sites';
  }

  login(): void {
    this.authService.login(this.username, this.password).subscribe(
      () => {
        this.router.navigateByUrl(this.returnUrl);
      },
      (error) => {
        console.error('Erreur de login', error);
        this.errorMessage = error.error instanceof ErrorEvent
          ? 'Erreur réseau: Veuillez réessayer plus tard.'
          : 'Erreur de login: Nom d\'utilisateur ou mot de passe incorrect.';
        alert(this.errorMessage);
      }
    );
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  // Méthode pour afficher/masquer le mot de passe
  togglePasswordVisibility(): void {
    this.passwordVisible = !this.passwordVisible;
  }
}

