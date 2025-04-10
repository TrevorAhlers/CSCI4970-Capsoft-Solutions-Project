import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrl: './registration.component.scss',
  standalone: false,
})
export class RegistrationComponent {
    constructor(private router: Router) {}
    createAnAccount = new FormGroup({
        username: new FormControl(''),
        email:new FormControl(''),
        password: new FormControl(''),
        confirm_password: new FormControl('')
      })


    createAccount(){
      this.router.navigateByUrl('/login');
    }

    createUser(){
      
    }
}
