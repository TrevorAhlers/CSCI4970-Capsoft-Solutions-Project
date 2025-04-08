import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
	selector: 'app-upload',
	templateUrl: './upload.component.html',
	styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
	constructor(private http: HttpClient) {}
  
	onFileSelected(event: any) {
	  const file = event.target.files[0];
	  if (file) {
		const formData = new FormData();
		formData.append('file', file, file.name);  
  
		// Send the file to the backend
		this.http.post('http://localhost:5000/upload', formData).subscribe(
		  (response: any) => {
			console.log('File uploaded successfully:', response);
		  },
		  (error) => {
			console.error('Error uploading file:', error);
		  }
		);
	  }
	}
  }
  
