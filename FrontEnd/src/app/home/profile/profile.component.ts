import { Component } from '@angular/core';
import { DataService } from '@services/data.service';
import { Router } from '@angular/router';

@Component({
    selector: 'app-profile',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.scss']
})

export class ProfileComponent {

  data: any;
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

  navigateToHome() {
    this.router.navigate(['/home']);
  }

  navigateToLogin() {
    this.router.navigateByUrl('/login');
  }
}