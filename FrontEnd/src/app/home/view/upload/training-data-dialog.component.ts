import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

interface TrainingInfo {
	files: string[];
}

@Component({
	selector: 'app-training-data-dialog',
	templateUrl: './training-data-dialog.component.html'
})
export class TrainingDataDialogComponent {
	files: string[] = [];
	uploading = false;
	uploadError = '';

	constructor(
		private http: HttpClient,
		public dialogRef: MatDialogRef<TrainingDataDialogComponent>,
		@Inject(MAT_DIALOG_DATA) public data: any
	) {
		this.refresh();
	}

	private refresh(): void {
		this.http
			.get<TrainingInfo>(`${environment.apiBaseUrl}/training/files`)
			.subscribe(d => (this.files = d.files));
	}

	uploadFile(event: Event): void {
		this.uploadError = '';
		const file = (event.target as HTMLInputElement).files?.[0];
		if (!file) return;

		if (!file.name.toLowerCase().endsWith('.csv')) {
			this.uploadError = 'Only CSV files are allowed.';
			return;
		}

		const form = new FormData();
		form.append('file', file, file.name);
		this.uploading = true;

		this.http.post(`${environment.apiBaseUrl}/training/upload`, form)
			.subscribe({
				next: () => {
					this.uploading = false;
					this.refresh();
				},
				error: () => {
					this.uploading = false;
					this.uploadError = 'Upload failed. Please try again.';
				}
			});
	}

	resetDefaults(): void {
		this.http.post(`${environment.apiBaseUrl}/training/reset`, {})
			.subscribe(() => this.refresh());
	}

	close(): void {
		this.dialogRef.close();
	}
}
