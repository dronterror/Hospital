import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadChildren: () => import('./features/dashboard/dashboard.module').then(m => m.DashboardModule)
  },
  {
    path: 'appointments',
    loadChildren: () => import('./features/appointments/appointments.module').then(m => m.AppointmentsModule)
  },
  {
    path: 'patients',
    loadChildren: () => import('./features/patients/patients.module').then(m => m.PatientsModule)
  },
  {
    path: 'doctors',
    loadChildren: () => import('./features/doctors/doctors.module').then(m => m.DoctorsModule)
  },
  {
    path: 'medical-records',
    loadChildren: () => import('./features/medical-records/medical-records.module').then(m => m.MedicalRecordsModule)
  },
  {
    path: 'prescriptions',
    loadChildren: () => import('./features/prescriptions/prescriptions.module').then(m => m.PrescriptionsModule)
  },
  {
    path: 'lab-results',
    loadChildren: () => import('./features/lab-results/lab-results.module').then(m => m.LabResultsModule)
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { } 