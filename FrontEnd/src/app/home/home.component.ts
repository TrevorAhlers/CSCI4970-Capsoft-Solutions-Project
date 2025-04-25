import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';

@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
	selectedCourse: any = null;
	selectedView: string = 'upload';
	private _selectedCourse: any = null;
	showSidebar = true;

	constructor(private dataService: DataService) {}

	ngOnInit(): void {
		this.dataService.getCourses().subscribe((data) => {
			console.log('Fetched courses in Home:', data);
		});
	}

	onCourseSelected(courseId: string): void {
		console.log('Course selected in home:', courseId);
		this.fetchCourseDetails(courseId);
	}

	fetchCourseDetails(courseId: string): void {
		this.dataService.getCourseDetails(courseId).subscribe(
			(data) => {
				console.log('Course details fetched:', data);
				this.selectedCourse = data;
	
				console.log('Fetching editable fields for:', courseId);
				this.dataService.getEditableCourseData(courseId).subscribe(
					(editData) => {
						console.log('Edit data fetched:', editData);
						this.selectedCourse.edit = editData;
						this.selectedCourse = { ...this.selectedCourse };
						this.dataService.setCourse(data);
					},
					(error) => {
						console.error('Error fetching editable course data:', error);
					}
				);
			},
			(error) => {
				console.error('Error fetching course details:', error);
			}
		);
	}
	
	saveCourseChanges(updated: any): void {
		console.log('Sending save data:', updated);
		this.dataService.saveEditedCourseData(updated.id, updated).subscribe(
			(res) => {
				console.log('Save successful:', res);
	
				this.dataService.triggerRefresh();
				this.dataService.triggerConflictRefresh();
	
				this.fetchCourseDetails(updated.id);
			},
			(err) => console.error('Save failed:', err)
		);
	}
	

	changeView(event: Event): void {
		const view = (event.target as HTMLSelectElement).value;
		this.selectedView = view;
	}
	savecourse() {
		this.dataService.setCourse(this.selectedCourse);
	  }



	toggleSidebar(): void {
		this.showSidebar = !this.showSidebar;
	  }
}
