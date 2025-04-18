import {
	Component,
	OnInit,
	ViewChild,
	Output,
	EventEmitter,
	AfterViewInit,
	ChangeDetectorRef
  } from '@angular/core';
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
  
	/* <‑‑ current selection – used for row highlight */
	selectedId: string | null = null;
  
	@ViewChild(MatSort) sort!: MatSort;
	@Output() rowClicked = new EventEmitter<string>();
  
	constructor(
	  private http: HttpClient,
	  private cdr: ChangeDetectorRef
	) {}
  
	/* ---------------- lifecycle ------------------- */
  
	ngOnInit(): void {
	  this.loadCourses();
	}
  
	ngAfterViewInit(): void {
	  this.filteredCourses.sort = this.sort;
	  this.cdr.detectChanges();
	}
  
	/* ---------------- data load ------------------ */
  
	loadCourses(): void {
	  this.http.get<any>('/api/data').subscribe((data) => {
		this.courses = data.courses;
		this.filteredCourses.data = this.courses;
  
		if (this.courses.length > 0) {
		  const keys = Object.keys(this.courses[0]);
		  this.displayedColumns = ['id', ...keys.filter(k => k !== 'id')];
		}
	  });
	}
  
	/* ---------------- filter --------------------- */
  
	applyFilter(event: Event): void {
	  const value = (event.target as HTMLInputElement).value.trim().toLowerCase();
	  this.filteredCourses.filter = value;
	}
  
	/* ---------------- row click ------------------ */
  
	handleRowClick(courseId: string): void {
	  this.selectedId = courseId;
	  this.rowClicked.emit(courseId);
	}
  }
  