import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DataService {
  private refreshTrigger = new Subject<void>();
  refresh$ = this.refreshTrigger.asObservable();
  private _selectedCourse: any = null;

  private conflictRefreshTrigger = new Subject<void>();
  conflictRefresh$ = this.conflictRefreshTrigger.asObservable();

  constructor(private http: HttpClient) {}

  getCourses(): Observable<any> {
    return this.http.get<any>('/api/data');
  }

  getCourseDetails(courseId: string): Observable<any> {
    return this.http.get<any>(`/details/${courseId}`);
  }

  triggerRefresh(): void {
    this.refreshTrigger.next();
  }

  triggerConflictRefresh(): void {
    this.conflictRefreshTrigger.next();
  }
  setCourse(course: any) {
    this._selectedCourse = course;
  }

  getCourse(): any {
    return this._selectedCourse;
  }
}
