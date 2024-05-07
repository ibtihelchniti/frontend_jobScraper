import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private apiUrl = "http://127.0.0.1:5000";

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    return this.http.post(`${this.apiUrl}/login`, formData);  
  }
  

  logout(): Observable<any> {
    return this.http.get(`${this.apiUrl}/logout`);
  }
}
