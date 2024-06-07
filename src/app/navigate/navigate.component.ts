import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../authentication.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navigate',
  templateUrl: './navigate.component.html',
  styleUrls: ['./navigate.component.css'] 
})
export class NavigateComponent implements OnInit {
  isAuthenticated: boolean = false; 
  showSubMenu: boolean = false;

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
