import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TrainingDataService {

  constructor(private http: HttpClient) {}

  list(): Observable<string[]> {
    return this.http.get<string[]>(`${environment.apiBaseUrl}/training-files`);
  }

  upload(file: File): Observable<void> {
    const fd = new FormData();
    fd.append('file', file, file.name);
    return this.http.post<void>(`${environment.apiBaseUrl}/training-upload`, fd);
  }

  reset(): Observable<void> {
    return this.http.post<void>(`${environment.apiBaseUrl}/training-reset`, {});
  }
}
