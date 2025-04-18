import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
	selector: 'app-conflict-card',
	templateUrl: './conflict-card.component.html',
	styleUrls: ['./conflict-card.component.scss']
})
export class ConflictCardComponent {
	@Input() conflict!: { id: string; content: string; ignored: boolean };
	@Output() ignore = new EventEmitter<string>();
	@Output() restore = new EventEmitter<string>();

	handleIgnore() {
		this.ignore.emit(this.conflict.id);
	}

	handleRestore() {
		this.restore.emit(this.conflict.id);
	}
}
