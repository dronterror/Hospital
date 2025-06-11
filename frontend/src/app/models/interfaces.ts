export interface User {
  id: number;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
}

export interface Doctor {
  id: number;
  user: User;
  specialization: string;
  bio: string;
  image?: string;
}

export interface Patient {
  id: number;
  user: User;
  dateOfBirth?: string;
  phoneNumber?: string;
  address?: string;
}

export interface Appointment {
  id: number;
  patient: Patient;
  doctor: Doctor;
  dateTime: string;
  status: 'SCHEDULED' | 'COMPLETED' | 'CANCELLED';
  reason: string;
  notes?: string;
}

export interface DoctorSchedule {
  id: number;
  doctor: Doctor;
  date: string;
  startTime: string;
  endTime: string;
  isAvailable: boolean;
} 