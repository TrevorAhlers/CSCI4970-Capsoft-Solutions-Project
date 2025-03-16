import { Component, OnInit } from '@angular/core';
import { DataService } from './data.service';  // Import the data service
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
    this.dataService.getData().subscribe(
      (response) => {
        this.data = response;  // Store the response data in the component
      },
      (error) => {
        console.error('Error fetching data:', error);  // Handle errors
      }
    );
  }

  navigateToHome() {
    this.router.navigate(['/home']);
  }

  navigateToData() {
    this.router.navigate(['/data']);
  }
}