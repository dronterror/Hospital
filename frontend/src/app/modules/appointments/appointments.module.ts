import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';

// Material Imports
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatChipsModule } from '@angular/material/chips';
import { MatDialogModule } from '@angular/material/dialog';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { MatMenuModule } from '@angular/material/menu';
import { MatSnackBarModule } from '@angular/material/snack-bar';

import { AppointmentsComponent } from '../../components/appointments/appointments.component';
import { AppointmentDialogComponent } from '../../components/appointments/appointment-dialog.component';

@NgModule({
  declarations: [
    AppointmentsComponent,
    AppointmentDialogComponent
  ],
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    MatButtonModule,
    MatIconModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    MatChipsModule,
    MatDialogModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatSelectModule,
    MatMenuModule,
    MatSnackBarModule
  ],
  exports: [AppointmentsComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppointmentsModule { } 