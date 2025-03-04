import { Component, OnInit } from '@angular/core';
import { DataService } from './data.service';  // Import the data service
import { Router } from '@angular/router';

@Component({
    selector: 'app-data',
    templateUrl: './data.component.html',
    styleUrls: ['./data.component.scss'],
    standalone: false
})
export class DataComponent implements OnInit {

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


}