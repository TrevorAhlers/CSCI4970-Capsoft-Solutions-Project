import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import {MatTabsModule} from '@angular/material/tabs';
import {MatDividerModule} from '@angular/material/divider'

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
    standalone: false
})
export class HomeComponent implements OnInit {

  data: any;  // Variable to store the data
  profileImage:string = "Capture.png"
 
  
  constructor(private dataService: DataService, private router:Router) {}

  ngOnInit(): void {
    // Fetch data from the Flask backend
    this.dataService.getData().subscribe({
      next: (response: any) => {
        this.data = response;
      },
      error: (err: any) => {
        console.error('Error fetching data:', err);
      }
    });
  }

  navigateToData() {
    this.router.navigate(['/data']);
  }
}