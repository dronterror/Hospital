import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { HomeComponent } from '../../components/home/home.component';

@NgModule({
  declarations: [HomeComponent],
  imports: [
    CommonModule,
    RouterModule,
    MatButtonModule,
    MatCardModule
  ],
  exports: [HomeComponent]
})
export class HomeModule { } 