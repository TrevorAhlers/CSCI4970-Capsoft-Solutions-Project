import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
	selector: 'app-column-selector-dialog',
	templateUrl: './column-selector-dialog.component.html'
})
export class ColumnSelectorDialogComponent {
	columns: string[];

	constructor(
		public dialogRef: MatDialogRef<ColumnSelectorDialogComponent>,
		@Inject(MAT_DIALOG_DATA) public data: { allColumns: string[], selected: string[] }
	) {
		this.columns = [...data.selected];
	}

	toggleColumn(column: string): void {
		if (this.columns.includes(column)) {
			this.columns = this.columns.filter(c => c !== column);
		} else {
			this.columns.push(column);
		}
	}

	isChecked(column: string): boolean {
		return this.columns.includes(column);
	}

	save(): void {
		this.dialogRef.close(this.columns);
	}

	cancel(): void {
		this.dialogRef.close(null);
	}
}
