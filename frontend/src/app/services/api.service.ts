import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Patient, Doctor, Appointment } from '../models/interfaces';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // Patient endpoints
  getPatients(): Observable<Patient[]> {
    return this.http.get<Patient[]>(`${this.apiUrl}/patients/`);
  }

  getPatient(id: number): Observable<Patient> {
    return this.http.get<Patient>(`${this.apiUrl}/patients/${id}/`);
  }

  createPatient(patient: Omit<Patient, 'id'>): Observable<Patient> {
    return this.http.post<Patient>(`${this.apiUrl}/patients/`, patient);
  }

  updatePatient(id: number, patient: Partial<Patient>): Observable<Patient> {
    return this.http.put<Patient>(`${this.apiUrl}/patients/${id}/`, patient);
  }

  deletePatient(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/patients/${id}/`);
  }

  // Doctor endpoints
  getDoctors(): Observable<Doctor[]> {
    return this.http.get<Doctor[]>(`${this.apiUrl}/doctors/`);
  }

  getDoctor(id: number): Observable<Doctor> {
    return this.http.get<Doctor>(`${this.apiUrl}/doctors/${id}/`);
  }

  createDoctor(doctor: Omit<Doctor, 'id'>): Observable<Doctor> {
    return this.http.post<Doctor>(`${this.apiUrl}/doctors/`, doctor);
  }

  updateDoctor(id: number, doctor: Partial<Doctor>): Observable<Doctor> {
    return this.http.patch<Doctor>(`${this.apiUrl}/doctors/${id}/`, doctor);
  }

  deleteDoctor(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/doctors/${id}/`);
  }

  getDoctorAvailability(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/doctors/${id}/availability/`);
  }

  // Appointment endpoints
  getAppointments(): Observable<Appointment[]> {
    return this.http.get<Appointment[]>(`${this.apiUrl}/appointments/`);
  }

  getAppointment(id: number): Observable<Appointment> {
    return this.http.get<Appointment>(`${this.apiUrl}/appointments/${id}/`);
  }

  createAppointment(appointment: Partial<Appointment>): Observable<Appointment> {
    return this.http.post<Appointment>(`${this.apiUrl}/appointments/`, appointment);
  }

  updateAppointment(id: number, appointment: Partial<Appointment>): Observable<Appointment> {
    return this.http.put<Appointment>(`${this.apiUrl}/appointments/${id}/`, appointment);
  }

  deleteAppointment(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/appointments/${id}/`);
  }

  // Export appointments to CSV
  exportAppointmentsToCSV(): Observable<Blob> {
    return this.http.get(`${this.apiUrl}/appointments/export/`, {
      responseType: 'blob'
    });
  }
} 