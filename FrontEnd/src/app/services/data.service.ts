import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import { environment } from 'src/environments/environment';

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
		return this.http.get<any>(`${environment.apiBaseUrl}/api/data`);
	}

	getCourseDetails(courseId: string): Observable<any> {
		return this.http.get<any>(`${environment.apiBaseUrl}/details/${courseId}`);
	}

	getEditableCourseData(courseId: string): Observable<any> {
		return this.http.get<any>(`${environment.apiBaseUrl}/edit/${courseId}`);
	}

	saveEditedCourseData(courseId: string, data: any): Observable<any> {
		return this.http.post<any>(`${environment.apiBaseUrl}/edit/save/${courseId}`, data);
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

	getChangeLog(): Observable<string> {
	return this.http.get(`${environment.apiBaseUrl}/api/change-log`, { responseType: 'text' })
	}

	getCurrentUsername(): Observable<{ username:string }> {
		return this.http.get<{ username:string }>(
			`${environment.apiBaseUrl}/api/current-user`
		);
	}
}