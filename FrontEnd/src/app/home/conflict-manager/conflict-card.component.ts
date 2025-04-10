import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
	selector: 'app-conflict-card',
	templateUrl: './conflict-card.component.html',
	styleUrls: ['./conflict-card.component.scss']
})
export class ConflictCardComponent {
	@Input() content: string = '';
	@Output() ignore = new EventEmitter<void>();

	handleIgnore() {
		this.ignore.emit();
	}
}
