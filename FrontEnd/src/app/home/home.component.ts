import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef } from '@angular/core';

@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
	courses: any[] = [];
	profileImage: string = 'Capture.png';
	selectedView: string = 'upload';

	constructor(
		private dataService: DataService,
		private router: Router,
		private cdr: ChangeDetectorRef
	) {}

	changeView(event: Event) {
		const view = (event.target as HTMLSelectElement).value;
		this.selectedView = view;
		this.cdr.detectChanges();

		if (view === 'listview') {
			setTimeout(() => {
				this.dataService.triggerRefresh();
			});
		}
	}

	ngOnInit(): void {
		this.dataService.getCourses().subscribe(data => {
			this.courses = data.courses;
		});
	}
}
