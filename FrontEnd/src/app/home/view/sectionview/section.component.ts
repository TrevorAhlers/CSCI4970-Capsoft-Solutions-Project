import {
	Component,
	OnInit,
	ViewChild,
	Output,
	EventEmitter,
	AfterViewInit,
	ChangeDetectorRef,
	OnDestroy
} from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { ColumnSelectorDialogComponent } from './column-selector-dialog.component';
import { DataService } from '@services/data.service';
import { Subscription } from 'rxjs';
import { environment } from 'src/environments/environment';

@Component({
	selector: 'app-section-view',
	templateUrl: './section.component.html',
	styleUrls: ['./section.component.scss'],
})
export class SectionComponent implements OnInit, AfterViewInit, OnDestroy {
	courses: any[] = [];
	filteredCourses = new MatTableDataSource<any>();
	displayedColumns: string[] = [];
	allPossibleColumns: string[] = [];

	selectedId: string | null = null;

	@ViewChild(MatSort) sort!: MatSort;
	@Output() rowClicked = new EventEmitter<string>();

	private refreshSub!: Subscription;
	private readonly API = environment.apiBaseUrl;

	constructor(
		private http: HttpClient,
		private cdr: ChangeDetectorRef,
		private dialog: MatDialog,
		private dataService: DataService
	) {}

	ngOnInit(): void {
		this.fetchAllColumns();
		this.loadCourses();

		this.refreshSub = this.dataService.refresh$.subscribe(() => {
			this.loadCourses();
		});
	}

	ngAfterViewInit(): void {
		this.filteredCourses.sort = this.sort;
		this.cdr.detectChanges();
	}

	ngOnDestroy(): void {
		if (this.refreshSub) this.refreshSub.unsubscribe();
	}

	fetchAllColumns(): void {
		this.http.get<any>(`${this.API}/api/columns`).subscribe((data) => {
			this.allPossibleColumns = data.columns;
		});
	}

	loadCourses(): void {
		this.http.get<any>(`${this.API}/api/data`).subscribe((data) => {
			this.courses = data.courses;
			this.filteredCourses.data = this.courses;

			if (this.courses.length > 0) {
				const keys = Object.keys(this.courses[0]);
				this.displayedColumns = ['id', ...keys.filter(k => k !== 'id')];
			}
		});
	}

	loadCoursesWithColumns(columns: string[]): void {
		this.http.post<any>(`${this.API}/api/data/columns`, { columns }).subscribe((data) => {
			this.courses = data.courses;
			this.filteredCourses.data = this.courses;
			this.displayedColumns = ['id', ...columns];
		});
	}

	openColumnSelector(): void {
		const dialogRef = this.dialog.open(ColumnSelectorDialogComponent, {
			width: '40rem',
			data: {
				allColumns: this.allPossibleColumns,
				selected: this.displayedColumns.filter(col => col !== 'id')
			}
		});

		dialogRef.afterClosed().subscribe(result => {
			if (result) this.loadCoursesWithColumns(result);
		});
	}

	applyFilter(event: Event): void {
		const value = (event.target as HTMLInputElement).value.trim().toLowerCase();
		this.filteredCourses.filter = value;
	}

	handleRowClick(courseId: string): void {
		this.selectedId = courseId;
		this.rowClicked.emit(courseId);
	}
}
