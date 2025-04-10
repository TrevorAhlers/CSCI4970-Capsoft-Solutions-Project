import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss']
})
export class DetailsComponent {
  @Input() selectedCourse: any;
  courseDetailsHtml: string | null = null;

  ngOnChanges(): void {
    if (this.selectedCourse) {
      this.courseDetailsHtml = this.selectedCourse.content || null;
    }
  }
}
