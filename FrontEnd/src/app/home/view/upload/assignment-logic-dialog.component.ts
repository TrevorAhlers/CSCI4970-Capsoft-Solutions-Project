import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
	selector: 'app-assignment-logic-dialog',
	templateUrl: './assignment-logic-dialog.component.html',
})
export class AssignmentLogicDialogComponent {
	logicOptions = [
		{ label: 'Historical Assignment', value: 'historical', checked: true },
		{ label: 'Historical by Department', value: 'historical-dept', checked: true },
		{ label: 'Predictive', value: 'predictive', checked: true }
	];

	showError = false;

	constructor(
		public dialogRef: MatDialogRef<AssignmentLogicDialogComponent>,
		@Inject(MAT_DIALOG_DATA) public data: { selected: string[] }
	) {
		if (data.selected.length) {
			this.logicOptions.forEach(opt => (opt.checked = data.selected.includes(opt.value)));
		}
	}

	toggle(value: string): void {
		const opt = this.logicOptions.find(o => o.value === value);
		if (opt) opt.checked = !opt.checked;
		this.showError = false;
	}

	confirm(): void {
		const selected = this.logicOptions.filter(o => o.checked).map(o => o.value);
		if (!selected.length) {
			this.showError = true;
			return;
		}
		this.dialogRef.close(selected);
	}

	cancel(): void {
		this.dialogRef.close();
	}
}
