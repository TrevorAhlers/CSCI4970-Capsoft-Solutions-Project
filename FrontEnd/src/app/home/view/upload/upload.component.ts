import { Component, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatDialog } from '@angular/material/dialog';
import { finalize } from 'rxjs/operators';

import { environment } from 'src/environments/environment';
import { DataService } from '@services/data.service';

import { AssignmentLogicDialogComponent } from './assignment-logic-dialog.component';
import { TrainingDataDialogComponent } from './training-data-dialog.component';

@Component({
	selector: 'app-upload',
	templateUrl: './upload.component.html',
	styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
	@Output() fileUploaded = new EventEmitter<void>();

	loading = false;
	selectedLogic: string[] = [];
	manualOverride = false;

	constructor(
		private http: HttpClient,
		private dataService: DataService,
		private dialog: MatDialog
	) {}

	onFileSelected(evt: any): void {
		const f = evt.target.files[0];
		if (!f) return;

		const form = new FormData();
		form.append('file', f, f.name);

		if (this.manualOverride) {
			form.append('logic', '__manual_only__');
		} else if (this.selectedLogic.length > 0) {
			form.append('logic', JSON.stringify(this.selectedLogic));
		}

		this.loading = true;
		this.http
			.post(`${environment.apiBaseUrl}/upload`, form)
			.pipe(finalize(() => (this.loading = false)))
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
		const ref = this.dialog.open(AssignmentLogicDialogComponent, {
			width: '30rem',
			data: { selected: this.selectedLogic }
		});

		ref.afterClosed().subscribe((res: string[]) => {
			if (res) this.selectedLogic = res;
		});
	}

	openTrainingDataDialog(): void {
		this.dialog.open(TrainingDataDialogComponent, { width: '32rem' });
	}
}
