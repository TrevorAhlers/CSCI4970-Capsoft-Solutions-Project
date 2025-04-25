import { Component, Input, Output, EventEmitter, OnChanges, ElementRef, ViewChild, AfterViewInit } from '@angular/core';

@Component({
	selector: 'app-details',
	templateUrl: './details.component.html',
	styleUrls: ['./details.component.scss']
})
export class DetailsComponent implements OnChanges, AfterViewInit {
	@Input() selectedCourse: any;
	@Output() saveClicked = new EventEmitter<any>();
	courseData: { label: string; value: string }[] = [];
	tab = 0;

	@ViewChild('htmlWrapper') htmlWrapperRef!: ElementRef;

	userInput = {
		room: '', meeting1: '', meeting2: '', meeting3: '', meeting4: '',
		crossListings: '', maxEnrollment: '', enrollment: '',
		comments: '', notes1: '', notes2: ''
	};

	ngOnChanges(): void {
		if (this.selectedCourse?.content) {
			const parser = new DOMParser();
			const doc = parser.parseFromString(this.selectedCourse.content, 'text/html');
			const pElements = Array.from(doc.querySelectorAll('p'));
	
			this.courseData = pElements.map(p => {
				const text = p.textContent ?? '';
				const [label, ...rest] = text.split(':');
				return { label: label.trim(), value: rest.join(':').trim() };
			});
		}
	
		if (this.selectedCourse?.edit) {
			this.userInput = {
				room: this.selectedCourse.edit.room || '',
				meeting1: this.selectedCourse.edit.meeting1 || '',
				crossListings: this.selectedCourse.edit.crossListings || '',
				maxEnrollment: this.selectedCourse.edit.maxEnrollment || '',
				enrollment: this.selectedCourse.edit.enrollment || '',
				comments: this.selectedCourse.edit.comments || '',
				notes1: this.selectedCourse.edit.notes1 || '',
				notes2: this.selectedCourse.edit.notes2 || '',
				meeting2: '', meeting3: '', meeting4: ''
			};
		}
	}

	save(): void {
		this.saveClicked.emit({
			id: this.selectedCourse?.edit?.id || this.selectedCourse?.id,
			...this.userInput
		});
	}

	ngAfterViewInit(): void {
		this.forceReflow();
	}

	switchTab(next: number): void {
		this.tab = next;
		this.forceReflow();
	}

	private forceReflow(): void {
		setTimeout(() => {
			if (this.htmlWrapperRef?.nativeElement) {
				this.htmlWrapperRef.nativeElement.style.display = 'none';
				this.htmlWrapperRef.nativeElement.offsetHeight;
				this.htmlWrapperRef.nativeElement.style.display = 'block';
			}
		}, 0);
	}
}
