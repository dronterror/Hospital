import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ApiService } from '../../services/api.service';
import { Doctor, Patient, Appointment } from '../../models/interfaces';

@Component({
  selector: 'app-appointment-dialog',
  template: `
    <h2 mat-dialog-title>{{ data.appointment ? 'Edit' : 'Book' }} Appointment</h2>
    <mat-dialog-content>
      <form [formGroup]="appointmentForm" class="appointment-form">
        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Doctor</mat-label>
          <mat-select formControlName="doctor" required>
            <mat-option *ngFor="let doctor of doctors" [value]="doctor.id">
              Dr. {{ doctor.user.firstName }} {{ doctor.user.lastName }} - {{ doctor.specialization }}
            </mat-option>
          </mat-select>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Date & Time</mat-label>
          <input matInput [matDatepicker]="picker" formControlName="dateTime" required>
          <mat-datepicker-toggle matSuffix [for]="picker"></mat-datepicker-toggle>
          <mat-datepicker #picker></mat-datepicker>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Reason</mat-label>
          <textarea matInput formControlName="reason" required rows="3"></textarea>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width">
          <mat-label>Notes</mat-label>
          <textarea matInput formControlName="notes" rows="2"></textarea>
        </mat-form-field>

        <mat-form-field appearance="outline" class="full-width" *ngIf="data.appointment">
          <mat-label>Status</mat-label>
          <mat-select formControlName="status" required>
            <mat-option value="SCHEDULED">Scheduled</mat-option>
            <mat-option value="COMPLETED">Completed</mat-option>
            <mat-option value="CANCELLED">Cancelled</mat-option>
          </mat-select>
        </mat-form-field>
      </form>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-button (click)="onCancel()">Cancel</button>
      <button mat-raised-button color="primary" (click)="onSubmit()" [disabled]="!appointmentForm.valid">
        {{ data.appointment ? 'Update' : 'Book' }}
      </button>
    </mat-dialog-actions>
  `,
  styles: [`
    .appointment-form {
      display: flex;
      flex-direction: column;
      gap: 16px;
      min-width: 400px;
      padding-top: 16px;
    }
    .full-width {
      width: 100%;
    }
  `]
})
export class AppointmentDialogComponent {
  appointmentForm: FormGroup;
  doctors: Doctor[] = [];

  constructor(
    private fb: FormBuilder,
    private apiService: ApiService,
    private dialogRef: MatDialogRef<AppointmentDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { appointment?: Appointment }
  ) {
    this.appointmentForm = this.fb.group({
      doctor: ['', Validators.required],
      dateTime: ['', Validators.required],
      reason: ['', Validators.required],
      notes: [''],
      status: ['SCHEDULED']
    });

    if (data.appointment) {
      this.appointmentForm.patchValue({
        doctor: data.appointment.doctor.id,
        dateTime: new Date(data.appointment.dateTime),
        reason: data.appointment.reason,
        notes: data.appointment.notes,
        status: data.appointment.status
      });
    }

    this.loadDoctors();
  }

  loadDoctors(): void {
    this.apiService.getDoctors().subscribe({
      next: (doctors) => {
        this.doctors = doctors;
      },
      error: (error) => {
        console.error('Error loading doctors:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.appointmentForm.valid) {
      const formValue = this.appointmentForm.value;
      const appointment = {
        ...formValue,
        dateTime: formValue.dateTime.toISOString()
      };

      if (this.data.appointment) {
        this.apiService.updateAppointment(this.data.appointment.id, appointment).subscribe({
          next: (result) => {
            this.dialogRef.close(result);
          },
          error: (error) => {
            console.error('Error updating appointment:', error);
          }
        });
      } else {
        this.apiService.createAppointment(appointment).subscribe({
          next: (result) => {
            this.dialogRef.close(result);
          },
          error: (error) => {
            console.error('Error creating appointment:', error);
          }
        });
      }
    }
  }

  onCancel(): void {
    this.dialogRef.close();
  }
} 