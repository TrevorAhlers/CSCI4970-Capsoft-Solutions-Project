import { Component, OnInit } from '@angular/core';
import { DataService } from './data.service';  // Import the data service

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  data: any;  // Variable to store the data

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    // Fetch data from the Flask backend
    this.dataService.getData().subscribe(
      (response) => {
        this.data = response;  // Store the response data in the component
        console.log(this.data);  // Log the response to the console (optional)
      },
      (error) => {
        console.error('Error fetching data:', error);  // Handle errors
      }
    );
  }
}