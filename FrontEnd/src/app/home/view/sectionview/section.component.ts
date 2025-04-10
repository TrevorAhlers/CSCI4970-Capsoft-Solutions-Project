import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { DataService } from '@services/data.service';

@Component({
	selector: 'app-section-view',
	templateUrl: './section.component.html',
	styleUrls: ['./section.component.scss'],
	standalone: false,
})
export class SectionComponent implements OnInit {
	courses: any[] = [];
	filteredCourses = new MatTableDataSource<any>();
	displayedColumns: string[] = [];

	@ViewChild(MatSort) sort!: MatSort;

	constructor(private dataService: DataService) {}

	ngOnInit(): void {
		this.loadCourses();

		this.dataService.refresh$.subscribe({
			next: () => this.loadCourses()
		});
	}

	loadCourses(): void {
		this.dataService.getCourses().subscribe({
			next: (data) => {
				this.courses = data.courses;
				this.filteredCourses.data = this.courses;

				if (this.courses.length > 0) {
					this.displayedColumns = Object.keys(this.courses[0]);
				}

				this.filteredCourses.sort = this.sort;
			}
		});
	}

	applyFilter(event: Event): void {
		const filterValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
		this.filteredCourses.filter = filterValue;
	}

	onRowClick(course: any): void {
		console.log('Row clicked:', course);
	}

	editCourse(course: any): void {
		console.log('Editing:', course);
	}

	deleteCourse(course: any): void {
		console.log('Deleting:', course);
	}

	viewCourse(course: any): void {
		console.log('Viewing:', course);
	}

	sortChanged(event: any): void {
		console.log('Sort changed:', event);
	}
}
