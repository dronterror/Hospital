import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

interface Service {
  id: number;
  name: string;
  description: string;
  price: number;
  duration: number;
}

@Component({
  selector: 'app-services',
  template: `
    <div class="container mt-4">
      <div class="d-flex justify-content-between mb-4">
        <h2>Medical Services</h2>
        <button mat-raised-button color="primary" (click)="addService()">
          <mat-icon>add</mat-icon>
          Add Service
        </button>
      </div>

      <mat-form-field>
        <mat-label>Filter</mat-label>
        <input matInput (keyup)="applyFilter($event)" placeholder="Ex. Cardiology" #input>
      </mat-form-field>

      <table mat-table [dataSource]="services" class="mat-elevation-z8">
        <ng-container matColumnDef="name">
          <th mat-header-cell *matHeaderCellDef> Name </th>
          <td mat-cell *matCellDef="let service"> {{service.name}} </td>
        </ng-container>

        <ng-container matColumnDef="description">
          <th mat-header-cell *matHeaderCellDef> Description </th>
          <td mat-cell *matCellDef="let service"> {{service.description}} </td>
        </ng-container>

        <ng-container matColumnDef="price">
          <th mat-header-cell *matHeaderCellDef> Price </th>
          <td mat-cell *matCellDef="let service"> {{service.price | currency}} </td>
        </ng-container>

        <ng-container matColumnDef="duration">
          <th mat-header-cell *matHeaderCellDef> Duration </th>
          <td mat-cell *matCellDef="let service"> {{service.duration}} minutes </td>
        </ng-container>

        <ng-container matColumnDef="actions">
          <th mat-header-cell *matHeaderCellDef> Actions </th>
          <td mat-cell *matCellDef="let service">
            <button mat-icon-button color="primary" (click)="editService(service)">
              <mat-icon>edit</mat-icon>
            </button>
            <button mat-icon-button color="warn" (click)="deleteService(service)">
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
    .container { margin-top: 20px; }
    table { width: 100%; }
    .mat-form-field { width: 100%; margin-bottom: 20px; }
    .mat-column-actions { width: 100px; }
  `]
})
export class ServicesComponent implements OnInit {
  services: Service[] = [];
  displayedColumns: string[] = ['name', 'description', 'price', 'duration', 'actions'];

  constructor(
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // Load services from backend
  }

  applyFilter(event: Event): void {
    const filterValue = (event.target as HTMLInputElement).value;
    // Apply filter to datasource
  }

  addService(): void {
    // Open dialog to add service
  }

  editService(service: Service): void {
    // Open dialog to edit service
  }

  deleteService(service: Service): void {
    // Show confirmation dialog and delete service
  }
} 