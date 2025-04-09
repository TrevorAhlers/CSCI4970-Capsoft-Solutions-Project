import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private apiUrl = 'http://localhost:5000/api/data'; // Flask port 5000 request

  constructor(private http: HttpClient) {}

  getCourses(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }

  getData(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
}