import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, tap, catchError } from 'rxjs';
import { environment } from '../../environments/environment';
import { AuthDto } from '../models/models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private user: AuthDto | null = null;
  private token: string | null = null;

  constructor(private http: HttpClient) {
    this.token = localStorage.getItem('token');
    if (this.token) {
      try {
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
      } catch (e) {}
    }
  }

  login(username: string, password: string): Observable<AuthDto> {
    const token = btoa(`${username}:${password}`);
    const headers = new HttpHeaders({ Authorization: `Basic ${token}` });
    return this.http.get<AuthDto>(`${environment.apiUrl}/auth/me`, { headers }).pipe(
      tap(user => {
        this.user = user;
        this.token = token;
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
      })
    );
  }

  logout() {
    this.user = null;
    this.token = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  getToken() { return this.token; }
  getUser() { return this.user; }
  isStaff() { return this.user?.role === 'ROLE_STAFF'; }
}