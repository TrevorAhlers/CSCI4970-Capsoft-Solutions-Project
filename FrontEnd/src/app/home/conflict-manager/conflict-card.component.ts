import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
	selector: 'app-conflict-card',
	templateUrl: './conflict-card.component.html',
	styleUrls: ['./conflict-card.component.scss']
})
export class ConflictCardComponent {

	@Input()  conflict!: { id: string; content: string; ignored: boolean };
	@Output() ignore	= new EventEmitter<string>();
	@Output() restore	= new EventEmitter<string>();

	handleIgnore(e: MouseEvent): void {
		e.stopPropagation();
		this.ignore.emit(this.conflict.id);
	}

	handleRestore(e: MouseEvent): void {
		e.stopPropagation();
		this.restore.emit(this.conflict.id);
	}
}
