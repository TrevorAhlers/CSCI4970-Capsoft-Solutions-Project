import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
	selector: 'app-section-row',
	templateUrl: './section-row.component.html',
	styleUrls: ['./section-row.component.scss']
})
export class SectionRowComponent {
	@Input() row!: Record<string, any>;
	@Input() columns: string[] = [];
	@Input() selected = false;

	@Output() clicked = new EventEmitter<string>();

	emitClick(): void {
		this.clicked.emit(this.row['id']);
	}
}
