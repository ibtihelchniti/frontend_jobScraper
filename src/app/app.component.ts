import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from './authentication.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  isAuthenticated: boolean = false; // Ajouter une variable pour suivre l'état de l'authentification

  constructor(public authService: AuthenticationService, private router: Router) {}

  ngOnInit(): void {
    this.authService.isAuthenticatedUser().subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
      if (!isAuthenticated) {
        this.router.navigate(['/login'], { skipLocationChange: true });
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
}

  getUsername(): string {
    return this.authService.getUsername();
  }

  
}
