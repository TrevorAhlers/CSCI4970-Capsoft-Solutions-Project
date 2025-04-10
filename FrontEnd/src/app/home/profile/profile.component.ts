import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent {
  profileImage: string = "Capture.png"; 

  constructor(private router: Router) {}

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
