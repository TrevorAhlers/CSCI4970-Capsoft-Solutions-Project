import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';

@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
	username: string = 'Guest User';
	selectedCourse: any = null;
	selectedView: string = 'upload';
	private _selectedCourse: any = null;
	showSidebar = true;

	constructor(private dataService: DataService) {}

ngOnInit(): void {
	// Fetch the current user's username
	this.dataService.getCurrentUsername()
		.subscribe((res: { username: string }) =>
			this.username = res?.username || 'Guest User'
		);

	// Optionally pre-fetch courses (for debugging)
	this.dataService.getCourses()
		.subscribe(data => console.log('Fetched courses in Home:', data));
}

onCourseSelected(courseId: string): void {
	console.log('Course selected in home:', courseId);
	this.fetchCourseDetails(courseId);
}

fetchCourseDetails(courseId: string): void {
	this.dataService.getCourseDetails(courseId).subscribe(
		data => {
			console.log('Course details fetched:', data);
			this.selectedCourse = data;

			console.log('Fetching editable fields for:', courseId);
			this.dataService.getEditableCourseData(courseId).subscribe(
				editData => {
					console.log('Edit data fetched:', editData);
					// Merge edit data into selectedCourse
					this.selectedCourse.edit = editData;
					// Trigger change detection by creating a new object reference
					this.selectedCourse = { ...this.selectedCourse };
					// Store in DataService if needed elsewhere
					this.dataService.setCourse(data);
				},
				error => console.error('Error fetching editable course data:', error)
			);
		},
		error => console.error('Error fetching course details:', error)
	);
}

saveCourseChanges(updated: any): void {
	console.log('Sending save data:', updated);
	this.dataService.saveEditedCourseData(updated.id, updated).subscribe(
		() => {
			console.log('Save successful');
			// Refresh both course list and conflicts
			this.dataService.triggerRefresh();
			this.dataService.triggerConflictRefresh();
			// Re-fetch details to update the sidebar view
			this.fetchCourseDetails(updated.id);
		},
		err => console.error('Save failed:', err)
	);
}

changeView(event: Event): void {
	this.selectedView = (event.target as HTMLSelectElement).value;
}

savecourse(): void {
	this.dataService.setCourse(this.selectedCourse);
}

toggleSidebar(): void {
	this.showSidebar = !this.showSidebar;
}
}
