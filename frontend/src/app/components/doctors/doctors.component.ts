import { Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { MatMenu } from '@angular/material/menu';
import { ApiService } from '../../services/api.service';
import { Doctor } from '../../models/interfaces';

@Component({
  selector: 'app-doctors',
  template: `
    <div class="doctors-container">
      <div class="header">
        <h1>Doctors</h1>
        <button mat-raised-button color="primary" (click)="openAddDialog()">
          <mat-icon>add</mat-icon>
          Add Doctor
        </button>
      </div>

      <mat-form-field appearance="outline" class="search-field">
        <mat-label>Search Doctors</mat-label>
        <input matInput (keyup)="applyFilter($event)" placeholder="Search by name or specialization..." #input>
        <mat-icon matSuffix>search</mat-icon>
      </mat-form-field>

      <div class="table-container mat-elevation-z8">
        <table mat-table [dataSource]="dataSource" matSort>
          <!-- Name Column -->
          <ng-container matColumnDef="name">
            <th mat-header-cell *matHeaderCellDef mat-sort-header> Name </th>
            <td mat-cell *matCellDef="let doctor"> 
              Dr. {{doctor.user.firstName}} {{doctor.user.lastName}}
            </td>
          </ng-container>

          <!-- Specialization Column -->
          <ng-container matColumnDef="specialization">
            <th mat-header-cell *matHeaderCellDef mat-sort-header> Specialization </th>
            <td mat-cell *matCellDef="let doctor"> {{doctor.specialization}} </td>
          </ng-container>

          <!-- Email Column -->
          <ng-container matColumnDef="email">
            <th mat-header-cell *matHeaderCellDef mat-sort-header> Email </th>
            <td mat-cell *matCellDef="let doctor"> {{doctor.user.email}} </td>
          </ng-container>

          <!-- Actions Column -->
          <ng-container matColumnDef="actions">
            <th mat-header-cell *matHeaderCellDef> Actions </th>
            <td mat-cell *matCellDef="let doctor">
              <button mat-icon-button [matMenuTriggerFor]="menu" aria-label="Actions">
                <mat-icon>more_vert</mat-icon>
              </button>
              <mat-menu #menu="matMenu">
                <button mat-menu-item (click)="editDoctor(doctor)">
                  <mat-icon>edit</mat-icon>
                  <span>Edit</span>
                </button>
                <button mat-menu-item (click)="deleteDoctor(doctor)">
                  <mat-icon color="warn">delete</mat-icon>
                  <span class="text-warn">Delete</span>
                </button>
              </mat-menu>
            </td>
          </ng-container>

          <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
          <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
        </table>

        <mat-paginator [pageSizeOptions]="[5, 10, 25, 100]" aria-label="Select page of doctors"></mat-paginator>
      </div>
    </div>
  `,
  styles: [`
    .doctors-container {
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

    .text-warn {
      color: #f44336;
    }

    .mat-row:hover {
      background-color: rgba(0, 0, 0, 0.04);
    }
  `]
})
export class DoctorsComponent implements OnInit {
  dataSource: MatTableDataSource<Doctor>;
  displayedColumns: string[] = ['name', 'specialization', 'email', 'actions'];

  @ViewChild(MatSort) sort!: MatSort;
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatMenu) menu!: MatMenu;

  constructor(
    private apiService: ApiService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {
    this.dataSource = new MatTableDataSource<Doctor>([]);
  }

  ngOnInit(): void {
    this.loadDoctors();
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
  }

  loadDoctors(): void {
    this.apiService.getDoctors().subscribe({
      next: (doctors: Doctor[]) => {
        this.dataSource.data = doctors;
      },
      error: (error: any) => {
        this.snackBar.open('Error loading doctors', 'Close', { duration: 3000 });
        console.error('Error loading doctors:', error);
      }
    });
  }

  deleteDoctor(doctor: Doctor): void {
    if (confirm(`Are you sure you want to delete Dr. ${doctor.user.firstName} ${doctor.user.lastName}?`)) {
      this.apiService.deleteDoctor(doctor.id).subscribe({
        next: () => {
          this.loadDoctors();
          this.snackBar.open('Doctor deleted successfully', 'Close', { duration: 3000 });
        },
        error: (error: any) => {
          this.snackBar.open('Error deleting doctor', 'Close', { duration: 3000 });
          console.error('Error deleting doctor:', error);
        }
      });
    }
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  openAddDialog(): void {
    // Implement add dialog logic
  }

  editDoctor(doctor: Doctor): void {
    // Implement edit dialog logic
  }
} 