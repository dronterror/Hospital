import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api.service';
import { Patient } from '../../models/interfaces';

@Component({
  selector: 'app-patients',
  template: `
    <div class="container">
      <div class="header">
        <h2>Patients</h2>
        <button mat-raised-button color="primary" (click)="openAddDialog()">
          <mat-icon>add</mat-icon>
          Add Patient
        </button>
      </div>

      <mat-form-field>
        <mat-label>Filter</mat-label>
        <input matInput (keyup)="applyFilter($event)" placeholder="Search patients..." #input>
      </mat-form-field>

      <table mat-table [dataSource]="patients" class="mat-elevation-z8">
        <!-- Name Column -->
        <ng-container matColumnDef="name">
          <th mat-header-cell *matHeaderCellDef> Name </th>
          <td mat-cell *matCellDef="let patient"> {{patient.firstName}} {{patient.lastName}} </td>
        </ng-container>

        <!-- Email Column -->
        <ng-container matColumnDef="email">
          <th mat-header-cell *matHeaderCellDef> Email </th>
          <td mat-cell *matCellDef="let patient"> {{patient.email}} </td>
        </ng-container>

        <!-- Phone Column -->
        <ng-container matColumnDef="phone">
          <th mat-header-cell *matHeaderCellDef> Phone </th>
          <td mat-cell *matCellDef="let patient"> {{patient.phone}} </td>
        </ng-container>

        <!-- Actions Column -->
        <ng-container matColumnDef="actions">
          <th mat-header-cell *matHeaderCellDef> Actions </th>
          <td mat-cell *matCellDef="let patient">
            <button mat-icon-button (click)="editPatient(patient)">
              <mat-icon>edit</mat-icon>
            </button>
            <button mat-icon-button color="warn" (click)="deletePatient(patient)">
              <mat-icon>delete</mat-icon>
            </button>
          </td>
        </ng-container>

        <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
        <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
      </table>
    </div>
  `,
  styles: [`
    .container {
      padding: 20px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    table {
      width: 100%;
    }
    mat-form-field {
      width: 100%;
      margin-bottom: 20px;
    }
  `]
})
export class PatientsComponent implements OnInit {
  patients: Patient[] = [];
  displayedColumns: string[] = ['name', 'email', 'phone', 'actions'];

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadPatients();
  }

  loadPatients(): void {
    this.apiService.getPatients().subscribe({
      next: (patients) => {
        this.patients = patients;
      },
      error: (error) => {
        this.snackBar.open('Error loading patients', 'Close', { duration: 3000 });
      }
    });
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    // Implement filtering logic here
  }

  openAddDialog(): void {
    // Implement add dialog logic
  }

  editPatient(patient: Patient): void {
    // Implement edit dialog logic
  }

  deletePatient(patient: Patient): void {
    if (confirm(`Are you sure you want to delete ${patient.firstName} ${patient.lastName}?`)) {
      this.apiService.deletePatient(patient.id).subscribe({
        next: () => {
          this.loadPatients();
          this.snackBar.open('Patient deleted successfully', 'Close', { duration: 3000 });
        },
        error: (error) => {
          this.snackBar.open('Error deleting patient', 'Close', { duration: 3000 });
        }
      });
    }
  }
} 