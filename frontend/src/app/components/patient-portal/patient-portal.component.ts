import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

interface Patient {
  id: number;
  name: string;
  email: string;
  phone: string;
  dateOfBirth: Date;
  medicalHistory: string;
}

@Component({
  selector: 'app-patient-portal',
  template: `
    <div class="container mt-4">
      <div class="row">
        <div class="col-md-4">
          <mat-card>
            <mat-card-header>
              <mat-card-title>Profile Information</mat-card-title>
            </mat-card-header>
            <mat-card-content>
              <div class="profile-info">
                <p><strong>Name:</strong> {{patient?.name}}</p>
                <p><strong>Email:</strong> {{patient?.email}}</p>
                <p><strong>Phone:</strong> {{patient?.phone}}</p>
                <p><strong>Date of Birth:</strong> {{patient?.dateOfBirth | date:'mediumDate'}}</p>
              </div>
            </mat-card-content>
            <mat-card-actions>
              <button mat-raised-button color="primary" (click)="editProfile()">
                <mat-icon>edit</mat-icon>
                Edit Profile
              </button>
            </mat-card-actions>
          </mat-card>
        </div>

        <div class="col-md-8">
          <mat-card>
            <mat-card-header>
              <mat-card-title>Medical History</mat-card-title>
            </mat-card-header>
            <mat-card-content>
              <p>{{patient?.medicalHistory}}</p>
            </mat-card-content>
          </mat-card>

          <mat-card class="mt-4">
            <mat-card-header>
              <mat-card-title>Upcoming Appointments</mat-card-title>
            </mat-card-header>
            <mat-card-content>
              <table mat-table [dataSource]="appointments" class="mat-elevation-z8">
                <ng-container matColumnDef="date">
                  <th mat-header-cell *matHeaderCellDef> Date </th>
                  <td mat-cell *matCellDef="let appointment"> {{appointment.date | date:'medium'}} </td>
                </ng-container>

                <ng-container matColumnDef="doctor">
                  <th mat-header-cell *matHeaderCellDef> Doctor </th>
                  <td mat-cell *matCellDef="let appointment"> {{appointment.doctor}} </td>
                </ng-container>

                <ng-container matColumnDef="service">
                  <th mat-header-cell *matHeaderCellDef> Service </th>
                  <td mat-cell *matCellDef="let appointment"> {{appointment.service}} </td>
                </ng-container>

                <ng-container matColumnDef="status">
                  <th mat-header-cell *matHeaderCellDef> Status </th>
                  <td mat-cell *matCellDef="let appointment">
                    <mat-chip-list>
                      <mat-chip [color]="getStatusColor(appointment.status)" selected>
                        {{appointment.status}}
                      </mat-chip>
                    </mat-chip-list>
                  </td>
                </ng-container>

                <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
                <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
              </table>
            </mat-card-content>
            <mat-card-actions>
              <button mat-raised-button color="primary" (click)="bookAppointment()">
                <mat-icon>add</mat-icon>
                Book Appointment
              </button>
            </mat-card-actions>
          </mat-card>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .container { max-width: 1200px; margin: 0 auto; }
    .profile-info { margin: 20px 0; }
    .profile-info p { margin: 10px 0; }
    table { width: 100%; margin-top: 20px; }
    .mat-column-status { width: 120px; }
  `]
})
export class PatientPortalComponent implements OnInit {
  patient: Patient | null = null;
  appointments: any[] = [];
  displayedColumns: string[] = ['date', 'doctor', 'service', 'status'];

  constructor(
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // Load patient data and appointments
  }

  editProfile(): void {
    // Open dialog to edit profile
  }

  bookAppointment(): void {
    // Open dialog to book appointment
  }

  getStatusColor(status: string): string {
    switch (status.toLowerCase()) {
      case 'confirmed':
        return 'primary';
      case 'pending':
        return 'accent';
      case 'cancelled':
        return 'warn';
      default:
        return '';
    }
  }
} 