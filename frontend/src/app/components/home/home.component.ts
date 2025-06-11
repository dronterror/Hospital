import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  template: `
    <div class="hero-section bg-primary text-white py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1 class="display-4 mb-4">Your Health, Our Priority</h1>
            <p class="lead mb-4">Experience world-class healthcare with our team of expert doctors and state-of-the-art facilities.</p>
            <button mat-raised-button color="accent" routerLink="/appointments">Book Appointment</button>
          </div>
          <div class="col-md-6">
            <img src="assets/images/hero-image.jpg" alt="Healthcare" class="img-fluid rounded shadow">
          </div>
        </div>
      </div>
    </div>

    <div class="services-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Our Services</h2>
        <div class="row">
          <div class="col-md-4 mb-4" *ngFor="let service of services">
            <mat-card>
              <img mat-card-image [src]="service.image" [alt]="service.name">
              <mat-card-content>
                <h3>{{service.name}}</h3>
                <p>{{service.description}}</p>
                <a [routerLink]="['/services', service.slug]" class="btn btn-link text-primary p-0">Learn More →</a>
              </mat-card-content>
            </mat-card>
          </div>
        </div>
      </div>
    </div>

    <div class="stats-section bg-light py-5">
      <div class="container">
        <div class="row text-center">
          <div class="col-md-3 mb-4">
            <h3 class="display-4 text-primary">50+</h3>
            <p class="text-muted">Expert Doctors</p>
          </div>
          <div class="col-md-3 mb-4">
            <h3 class="display-4 text-primary">10k+</h3>
            <p class="text-muted">Happy Patients</p>
          </div>
          <div class="col-md-3 mb-4">
            <h3 class="display-4 text-primary">24/7</h3>
            <p class="text-muted">Emergency Care</p>
          </div>
          <div class="col-md-3 mb-4">
            <h3 class="display-4 text-primary">15+</h3>
            <p class="text-muted">Years Experience</p>
          </div>
        </div>
      </div>
    </div>

    <div class="news-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Latest News</h2>
        <div class="row">
          <div class="col-md-4 mb-4" *ngFor="let news of latestNews">
            <mat-card>
              <img mat-card-image [src]="news.image" [alt]="news.title">
              <mat-card-content>
                <p class="text-muted small mb-2">{{news.date | date:'mediumDate'}}</p>
                <h3>{{news.title}}</h3>
                <p>{{news.excerpt}}</p>
                <a [routerLink]="['/news', news.slug]" class="btn btn-link text-primary p-0">Read More →</a>
              </mat-card-content>
            </mat-card>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .hero-section { background: linear-gradient(135deg, #0056b3 0%, #00a0dc 100%); }
    .services-section mat-card { height: 100%; }
    .stats-section .display-4 { font-weight: 600; }
    .news-section mat-card { height: 100%; }
    img { max-width: 100%; height: auto; }
  `]
})
export class HomeComponent implements OnInit {
  services = [
    {
      name: 'Primary Care',
      description: 'Comprehensive healthcare services for all your medical needs.',
      image: 'assets/images/primary-care.jpg',
      slug: 'primary-care'
    },
    {
      name: 'Specialized Care',
      description: 'Expert care in various medical specialties.',
      image: 'assets/images/specialized-care.jpg',
      slug: 'specialized-care'
    },
    {
      name: 'Emergency Care',
      description: '24/7 emergency medical services.',
      image: 'assets/images/emergency-care.jpg',
      slug: 'emergency-care'
    }
  ];

  latestNews = [
    {
      title: 'New Medical Center Opening',
      excerpt: 'We are excited to announce the opening of our new medical center.',
      image: 'assets/images/news1.jpg',
      date: new Date('2023-06-01'),
      slug: 'new-medical-center'
    },
    {
      title: 'COVID-19 Vaccination Update',
      excerpt: 'Latest updates on our COVID-19 vaccination program.',
      image: 'assets/images/news2.jpg',
      date: new Date('2023-05-28'),
      slug: 'covid-vaccination-update'
    },
    {
      title: 'Health Tips for Summer',
      excerpt: 'Stay healthy this summer with these important tips.',
      image: 'assets/images/news3.jpg',
      date: new Date('2023-05-25'),
      slug: 'summer-health-tips'
    }
  ];

  constructor() {}

  ngOnInit(): void {}
} 