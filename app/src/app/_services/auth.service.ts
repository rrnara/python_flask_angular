import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const AUTH_API = 'http://127.0.0.1:5000/api/auth/';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor(private http: HttpClient) { }

  login(username: string, password: string): Observable<any> {
    return this.http.post(AUTH_API + 'login', {
      username,
      password
    }, httpOptions);
  }

  register(name: string, username: string, password: string): Observable<any> {
    return this.http.post(AUTH_API + 'register', {
      name,
      username,
      password
    }, httpOptions);
  }

  updatePassword(password: string): Observable<any> {
    return this.http.post(AUTH_API + 'password', { password }, httpOptions);
  }

  // Only admin users can do this
  addAdmin(name: string, username: string, password: string): Observable<any> {
    return this.http.post(AUTH_API + 'admin', {
      name,
      username,
      password
    }, httpOptions);
  }
}
