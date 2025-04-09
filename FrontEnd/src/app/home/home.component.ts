import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import {MatTabsModule} from '@angular/material/tabs';
import {MatDividerModule} from '@angular/material/divider'
import { HttpClient } from '@angular/common/http';
import { ChangeDetectorRef } from '@angular/core';





@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
    standalone: false
})
export class HomeComponent implements OnInit {
  
  courses: any[] = [];

  constructor(private dataService: DataService, private router:Router, private cdr: ChangeDetectorRef) {}

 
  profileImage:string = "Capture.png"
  selectedView: string = 'upload'; 

  changeView(event: Event) {
    this.selectedView = (event.target as HTMLSelectElement).value;
    this.cdr.detectChanges();
  }

  ngOnInit(): void {
    this.dataService.getCourses().subscribe(data => {
      this.courses = data.courses;
    });

}
}
      
  