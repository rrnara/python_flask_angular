import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = 'http://127.0.0.1:5000/api/users/';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) { }

  getMe(): Observable<any> {
    return this.http.get(API_URL + 'me');
  }

  // Admin functions
  getAdmins(): Observable<any> {
    return this.http.get(API_URL + 'all?role=admin');
  }

  // Only admin users can do this
  addCleaner(badge: string, name: string): Observable<any> {
    return this.http.post(API_URL + 'cleaners', {
      badge,
      name
    }, httpOptions);
  }

  // For admin date is not needed, non-admins are checking availability on date format is yyyy-mm-dd
  getCleaners(date: string): Observable<any> {
    return this.http.get(API_URL + `cleaners?date=${date}`);
  }

  // only for non-admins, date format is yyyy-mm-dd
  addBooking(cleaner_id: number, date: string): Observable<any> {
    return this.http.post(API_URL + 'bookings', {
      cleaner_id,
      date
    }, httpOptions);
  }

  // For non-admin date is not needed (gets all future bookings), admins are checking bookings on date format is yyyy-mm-dd
  getBookings(date: string): Observable<any> {
    return this.http.get(API_URL + `bookings?date=${date}`);
  }
}
