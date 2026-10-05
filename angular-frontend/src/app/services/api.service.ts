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