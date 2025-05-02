import { Component, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { AssignmentLogicDialogComponent } from './assignment-logic-dialog.component';
import { DataService } from '@services/data.service';
import { environment } from 'src/environments/environment';
import { finalize } from 'rxjs/operators';

@Component({
	selector: 'app-upload',
	templateUrl: './upload.component.html',
	styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
	@Output() fileUploaded = new EventEmitter<void>();
	loading = false;
	selectedLogic: string[] = [];

	constructor(
		private http: HttpClient,
		private dataService: DataService,
		private dialog: MatDialog
	) {}

	onFileSelected(event: any) {
		const file = event.target.files[0];
		if (!file) return;

		const formData = new FormData();
		formData.append('file', file, file.name);
		formData.append('logic', JSON.stringify(this.selectedLogic));

		this.loading = true;
		this.http.post(`${environment.apiBaseUrl}/upload`, formData)
			.pipe(finalize(() => this.loading = false))
			.subscribe({
				next: () => {
					this.dataService.triggerRefresh();
					this.dataService.triggerConflictRefresh();
					this.fileUploaded.emit();
				},
				error: err => console.error('Error uploading file:', err)
			});
	}

	openLogicSelector(): void {
		const dialogRef = this.dialog.open(AssignmentLogicDialogComponent, {
			width: '30rem',
			data: { selected: this.selectedLogic }
		});

		dialogRef.afterClosed().subscribe((result: string[]) => {
			if (result) this.selectedLogic = result;
		});
	}
}
