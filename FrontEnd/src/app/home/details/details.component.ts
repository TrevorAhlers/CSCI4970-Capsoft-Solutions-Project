import { Component, Input, OnChanges } from '@angular/core';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss']
})


export class DetailsComponent {
  @Input() selectedCourse: any;
  courseDetailsHtml: string | null = null;
  userInput1: string = '';
  userInput2: string = '';
  userInput3: string = '';
  userInput4: string = '';
  userInput5: string = '';
  userInput6: string = '';
  userInput7: string = '';
  userInput8: string = '';
  userInput9: string = '';
  userInput10: string = '';

  ngOnChanges(): void {
    if (this.selectedCourse) {
      this.courseDetailsHtml = this.selectedCourse.content || null;
    }
  }
}
