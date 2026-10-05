import os

base = "angular-frontend/src/app"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip())

# Environment
write_file("angular-frontend/src/environments/environment.ts", """
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080/api'
};
""")

# Models
write_file(f"{base}/models/models.ts", """
export interface ZoneDto {
  id: number;
  name: string;
  valveState: string;
}
export interface ReadingDto {
  waterLevel: number;
  recordedAt: string;
}
export interface AlertDto {
  id: number;
  zoneName: string;
  severity: string;
  geminiExplanation: string;
  priority: number;
  recommendedAction: string;
  ticketId: number;
  ticketStatus: string;
}
export interface ComplaintDto {
  zoneId: number;
  description: string;
  category: string;
  priority: string;
}
export interface AuthDto {
  username: string;
  role: string;
}
""")

# Services
write_file(f"{base}/services/api.service.ts", """
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ZoneDto, ReadingDto, AlertDto, ComplaintDto } from '../models/models';

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}
  
  getZones(): Observable<ZoneDto[]> {
    return this.http.get<ZoneDto[]>(`${environment.apiUrl}/zones`);
  }
  getAlerts(severity?: string): Observable<AlertDto[]> {
    let url = `${environment.apiUrl}/alerts`;
    if (severity) url += `?severity=${severity}`;
    return this.http.get<AlertDto[]>(url);
  }
  getReadings(zoneId: number): Observable<ReadingDto[]> {
    return this.http.get<ReadingDto[]>(`${environment.apiUrl}/zones/${zoneId}/readings`);
  }
  createComplaint(complaint: ComplaintDto): Observable<any> {
    return this.http.post(`${environment.apiUrl}/complaints`, complaint);
  }
  resolveTicket(ticketId: number, notes: string): Observable<any> {
    return this.http.put(`${environment.apiUrl}/tickets/${ticketId}`, { status: 'RESOLVED', notes });
  }
  deleteAlert(alertId: number): Observable<any> {
    return this.http.delete(`${environment.apiUrl}/alerts/${alertId}`);
  }
}
""")

write_file(f"{base}/services/auth.service.ts", """
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
""")

write_file(f"{base}/services/auth.interceptor.ts", """
import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private auth: AuthService) {}
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.auth.getToken();
    if (token) {
      request = request.clone({
        setHeaders: { Authorization: `Basic ${token}` }
      });
    }
    return next.handle(request);
  }
}
""")

print("Angular script generated!")
