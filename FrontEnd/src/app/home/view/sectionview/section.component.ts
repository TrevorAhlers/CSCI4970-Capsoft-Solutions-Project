import { Component, OnInit, ViewChild } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { DataService } from '@services/data.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop'
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatCardModule } from '@angular/material/card';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';





@Component({
	selector: 'app-section-view',
	templateUrl: './section.component.html',
	styleUrls: ['./section.component.scss'],
	standalone: false,
})
export class SectionComponent {
	courses: any[] = [];
	filteredCourses = new MatTableDataSource<any>();
	displayedColumns: string[] = [];
  
	@ViewChild(MatSort) sort!: MatSort;
  
	constructor(private dataService: DataService) {}
  
	ngOnInit(): void {
	  this.dataService.getCourses().subscribe(data => {
		this.courses = data.courses;
		this.filteredCourses.data = this.courses;
  
		// Dynamically set columns based on course data
		if (this.courses.length > 0) {
		  this.displayedColumns = Object.keys(this.courses[0]);
		}
  
		// Apply sorting functionality
		this.filteredCourses.sort = this.sort;
	  });
	}
  
	// Filter the table data
	applyFilter(event: Event): void {
	  const filterValue = (event.target as HTMLInputElement).value.trim().toLowerCase();
	  this.filteredCourses.filter = filterValue;
	}
  
	// Log the row click
	onRowClick(course: any): void {
	  console.log('Row clicked:', course);
	}
  
	// Edit course action
	editCourse(course: any): void {
	  console.log('Editing:', course);
	}
  
	// Delete course action
	deleteCourse(course: any): void {
	  console.log('Deleting:', course);
	}
  
	// View course action
	viewCourse(course: any): void {
	  console.log('Viewing:', course);
	}
  
	// Handle sorting changes
	sortChanged(event: any): void {
	  console.log('Sort changed:', event);
	}
  }