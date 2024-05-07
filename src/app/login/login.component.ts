import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from '../authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  isAuthenticated: boolean = false; // Ajouter une variable pour suivre l'état de l'authentification

  constructor(private authService: AuthenticationService, private router: Router) {}

  login(): void {
    this.authService.login(this.username, this.password).subscribe(
        (response) => {
            alert(response.message);  // Afficher le message de la réponse
            this.isAuthenticated = true; // Mettre à jour l'état de l'authentification
            this.router.navigate(['/site-list']);  // Rediriger vers la liste des sites après le login réussi
        },
        (error) => {
            console.error('Erreur de login', error);
            alert('Erreur de login : ' + error.message); // Afficher l'erreur localement
        }
    );
  }
  
}
