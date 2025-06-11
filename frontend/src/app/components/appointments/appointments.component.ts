import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTable } from '@angular/material/table';
import { ApiService } from '../../services/api.service';
import { Appointment } from '../../models/interfaces';
import { AppointmentDialogComponent } from './appointment-dialog.component';

@Component({
  selector: 'app-appointments',
  template: `
    <div class="appointments-container">
      <div class="header">
        <h1>Appointments</h1>
        <div class="header-actions">
          <button mat-raised-button color="accent" (click)="exportToCSV()">
            <mat-icon>download</mat-icon>
            Export to CSV
          </button>
          <button mat-raised-button color="primary" (click)="openAddDialog()">
            <mat-icon>add</mat-icon>
            Book Appointment
          </button>
        </div>
      </div>

      <mat-form-field appearance="outline" class="search-field">
        <mat-label>Search Appointments</mat-label>
        <input matInput (keyup)="applyFilter($event)" placeholder="Search by patient, doctor, or status..." #input>
        <mat-icon matSuffix>search</mat-icon>
      </mat-form-field>

      <div class="table-container mat-elevation-z8">
        <table mat-table [dataSource]="appointments" matSort>
          <!-- Date Column -->
          <ng-container matColumnDef="date">
            <th mat-header-cell *matHeaderCellDef mat-sort-header> Date & Time </th>
            <td mat-cell *matCellDef="let appointment"> 
              {{appointment.dateTime | date:'medium'}} 
            </td>
          </ng-container>

          <!-- Patient Column -->
          <ng-container matColumnDef="patient">
            <th mat-header-cell *matHeaderCellDef mat-sort-header> Patient </th>
            <td mat-cell *matCellDef="let appointment"> 
              {{appointment.patient.user.firstName}} {{appointment.patient.user.lastName}}
            </td>
          </ng-container>

          <!-- Doctor Column -->
          <ng-container matColumnDef="doctor">
            <th mat-header-cell *matHeaderCellDef mat-sort-header> Doctor </th>
            <td mat-cell *matCellDef="let appointment"> 
              Dr. {{appointment.doctor.user.firstName}} {{appointment.doctor.user.lastName}}
            </td>
          </ng-container>

          <!-- Status Column -->
          <ng-container matColumnDef="status">
            <th mat-header-cell *matHeaderCellDef mat-sort-header> Status </th>
            <td mat-cell *matCellDef="let appointment">
              <mat-chip-list>
                <mat-chip [color]="getStatusColor(appointment.status)" selected>
                  {{appointment.status | titlecase}}
                </mat-chip>
              </mat-chip-list>
            </td>
          </ng-container>

          <!-- Actions Column -->
          <ng-container matColumnDef="actions">
            <th mat-header-cell *matHeaderCellDef> Actions </th>
            <td mat-cell *matCellDef="let appointment">
              <button mat-icon-button [matMenuTriggerFor]="menu" aria-label="Actions">
                <mat-icon>more_vert</mat-icon>
              </button>
              <mat-menu #menu="matMenu">
                <button mat-menu-item (click)="editAppointment(appointment)">
                  <mat-icon>edit</mat-icon>
                  <span>Edit</span>
                </button>
                <button mat-menu-item (click)="deleteAppointment(appointment)">
                  <mat-icon color="warn">delete</mat-icon>
                  <span class="text-warn">Delete</span>
                </button>
              </mat-menu>
            </td>
          </ng-container>

          <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
          <tr mat-row *matRowDef="let row; columns: displayedColumns;"
              [class.cancelled]="row.status === 'CANCELLED'"></tr>
        </table>

        <mat-paginator [pageSizeOptions]="[5, 10, 25, 100]" aria-label="Select page of appointments"></mat-paginator>
      </div>
    </div>
  `,
  styles: [`
    .appointments-container {
      padding: 24px;
      max-width: 1200px;
      margin: 0 auto;
    }

    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
    }

    h1 {
      font-size: 2rem;
      font-weight: 500;
      margin: 0;
      color: #1a237e;
    }

    .header-actions {
      display: flex;
      gap: 12px;
    }

    .search-field {
      width: 100%;
      margin-bottom: 24px;
    }

    .table-container {
      border-radius: 8px;
      overflow: hidden;
    }

    table {
      width: 100%;
    }

    .mat-column-actions {
      width: 80px;
      text-align: center;
    }

    .mat-column-status {
      width: 120px;
    }

    .text-warn {
      color: #f44336;
    }

    tr.cancelled {
      background-color: rgba(0, 0, 0, 0.04);
    }

    tr.cancelled td {
      color: rgba(0, 0, 0, 0.6);
    }

    .mat-row:hover {
      background-color: rgba(0, 0, 0, 0.04);
    }

    ::ng-deep .mat-chip.mat-standard-chip {
      min-height: 28px;
    }
  `]
})
export class AppointmentsComponent implements OnInit {
  appointments: Appointment[] = [];
  displayedColumns: string[] = ['date', 'patient', 'doctor', 'status', 'actions'];

  @ViewChild(MatTable) table!: MatTable<any>;

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadAppointments();
  }

  loadAppointments(): void {
    this.apiService.getAppointments().subscribe({
      next: (appointments) => {
        this.appointments = appointments;
        if (this.table) {
          this.table.renderRows();
        }
      },
      error: (error) => {
        this.snackBar.open('Error loading appointments', 'Close', { duration: 3000 });
        console.error('Error loading appointments:', error);
      }
    });
  }

  openAddDialog(): void {
    const dialogRef = this.dialog.open(AppointmentDialogComponent, {
      data: {}
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.loadAppointments();
        this.snackBar.open('Appointment booked successfully', 'Close', { duration: 3000 });
      }
    });
  }

  editAppointment(appointment: Appointment): void {
    const dialogRef = this.dialog.open(AppointmentDialogComponent, {
      data: { appointment }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.loadAppointments();
        this.snackBar.open('Appointment updated successfully', 'Close', { duration: 3000 });
      }
    });
  }

  deleteAppointment(appointment: Appointment): void {
    if (confirm('Are you sure you want to delete this appointment?')) {
      this.apiService.deleteAppointment(appointment.id).subscribe({
        next: () => {
          this.loadAppointments();
          this.snackBar.open('Appointment deleted successfully', 'Close', { duration: 3000 });
        },
        error: (error) => {
          this.snackBar.open('Error deleting appointment', 'Close', { duration: 3000 });
          console.error('Error deleting appointment:', error);
        }
      });
    }
  }

  getStatusColor(status: string): string {
    switch (status) {
      case 'SCHEDULED':
        return 'primary';
      case 'COMPLETED':
        return 'accent';
      case 'CANCELLED':
        return 'warn';
      default:
        return '';
    }
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value.toLowerCase();
    // Implement filtering logic here based on your requirements
  }

  exportToCSV(): void {
    this.apiService.exportAppointmentsToCSV().subscribe({
      next: (blob: Blob) => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `appointments_${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
        window.URL.revokeObjectURL(url);
        this.snackBar.open('Appointments exported successfully', 'Close', { duration: 3000 });
      },
      error: (error) => {
        this.snackBar.open('Error exporting appointments', 'Close', { duration: 3000 });
        console.error('Error exporting appointments:', error);
      }
    });
  }
} 