import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ContentService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getFeaturedServices(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/api/v1/services/?featured=true`);
  }

  getLatestNews(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/api/v1/wagtail/pages/?type=news.NewsPage&order=-first_published_at&limit=3`);
  }

  getService(slug: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/v1/services/${slug}/`);
  }

  getDoctors(params: any = {}): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/api/v1/doctors/`, { params });
  }

  makeAppointment(appointmentData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/api/v1/appointments/`, appointmentData);
  }
} 