import { Component, OnInit, ViewChild, Output, EventEmitter, AfterViewInit, ChangeDetectorRef } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { HttpClient } from '@angular/common/http';

@Component({
	selector: 'app-section-view',
	templateUrl: './section.component.html',
	styleUrls: ['./section.component.scss'],
})
export class SectionComponent implements OnInit, AfterViewInit {
	courses: any[] = [];
	filteredCourses = new MatTableDataSource<any>();
	displayedColumns: string[] = [];

	@ViewChild(MatSort) sort!: MatSort;
	@Output() rowClicked = new EventEmitter<any>();

	constructor(
		private http: HttpClient,
		private cdr: ChangeDetectorRef
	) {}

	ngOnInit(): void {
		this.loadCourses();
	}

	ngAfterViewInit(): void {
		this.filteredCourses.sort = this.sort;
		this.cdr.detectChanges();
	}

	loadCourses(): void {
		console.log('Fetching courses...');
		this.http.get<any>('/api/data').subscribe((data) => {
			console.log('Fetched courses:', data);
			this.courses = data.courses;
			this.filteredCourses.data = this.courses;

			if (this.courses.length > 0) {
				const keys = Object.keys(this.courses[0]);
				this.displayedColumns = ['id', ...keys.filter((k) => k !== 'id')];
			}
		});
	}

	applyFilter(event: Event): void {
		const filterValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
		this.filteredCourses.filter = filterValue;
	}

	handleRowClick(courseId: string): void {
		console.log('Row clicked, course id:', courseId);
		if (courseId) {
			this.rowClicked.emit(courseId);
		} else {
			console.error('Course id is missing:', courseId);
		}
	}
}
