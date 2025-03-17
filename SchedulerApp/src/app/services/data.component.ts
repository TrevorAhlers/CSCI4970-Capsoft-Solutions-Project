import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';
import { Router } from '@angular/router';

@Component({
    selector: 'app-data',
    templateUrl: './data.component.html',
    styleUrls: ['./data.component.scss'],
    standalone: false
})
export class DataComponent implements OnInit {

  courses: any[] = [];

  constructor(private dataService: DataService, private router:Router) {}

  ngOnInit(): void {
    this.dataService.getCourses().subscribe(data => {
      this.courses = data.courses;
    });
  }



  navigateToHome() {
    this.router.navigate(['/home']);
  }


}