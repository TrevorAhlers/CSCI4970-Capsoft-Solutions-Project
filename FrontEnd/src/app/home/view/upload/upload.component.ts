import { Component, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from '@services/data.service';

@Component({
	selector: 'app-upload',
	templateUrl: './upload.component.html',
	styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
	@Output() fileUploaded = new EventEmitter<void>();

	constructor(private http: HttpClient, private dataService: DataService) {}

	onFileSelected(event: any) {
		const file = event.target.files[0];
		if (file) {
			const formData = new FormData();
			formData.append('file', file, file.name);

			this.http.post('/upload', formData).subscribe({
				next: () => {
					this.dataService.triggerRefresh();
					this.dataService.triggerConflictRefresh();
					this.fileUploaded.emit(); // trigger parent view change
				},
				error: (err) => {
					console.error('Error uploading file:', err);
				}
			});
		}
	}
}
