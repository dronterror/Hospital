import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <mat-sidenav-container class="sidenav-container">
      <mat-sidenav #drawer class="sidenav" fixedInViewport
          [attr.role]="(isHandset$ | async) ? 'dialog' : 'navigation'"
          [mode]="(isHandset$ | async) ? 'over' : 'side'"
          [opened]="(isHandset$ | async) === false">
        <mat-toolbar>Menu</mat-toolbar>
        <mat-nav-list>
          <a mat-list-item routerLink="/dashboard">Dashboard</a>
          <a mat-list-item routerLink="/appointments">Appointments</a>
          <a mat-list-item routerLink="/patients">Patients</a>
          <a mat-list-item routerLink="/doctors">Doctors</a>
          <a mat-list-item routerLink="/medical-records">Medical Records</a>
          <a mat-list-item routerLink="/prescriptions">Prescriptions</a>
          <a mat-list-item routerLink="/lab-results">Lab Results</a>
        </mat-nav-list>
      </mat-sidenav>
      <mat-sidenav-content>
        <mat-toolbar color="primary">
          <button
            type="button"
            aria-label="Toggle sidenav"
            mat-icon-button
            (click)="drawer.toggle()">
            <mat-icon aria-label="Side nav toggle icon">menu</mat-icon>
          </button>
          <span>Hospital Management System</span>
        </mat-toolbar>
        <div class="content-container">
          <router-outlet></router-outlet>
        </div>
      </mat-sidenav-content>
    </mat-sidenav-container>
  `,
  styles: [`
    .sidenav-container {
      height: 100%;
    }
    
    .sidenav {
      width: 250px;
    }
    
    .content-container {
      padding: 20px;
    }
    
    .mat-toolbar.mat-primary {
      position: sticky;
      top: 0;
      z-index: 1;
    }
  `]
})
export class AppComponent {
  title = 'Hospital Management System';
} 