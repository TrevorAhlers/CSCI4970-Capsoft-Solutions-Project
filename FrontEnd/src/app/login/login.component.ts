// login.component.ts
import { Component, ComponentFactoryResolver } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
    standalone: false
})
export class LoginComponent {
  constructor(private router: Router) {}
  

  loginForm = new FormGroup({
    username: new FormControl(''),
    password: new FormControl('')
  })
  
  navigateToHome() {
    this.router.navigateByUrl('/home');
  }

  navigateToRegistration(){
    this.router.navigateByUrl('/registration');
    console.log("Does-s")
  }

  loginUser(){
    //Added Service to route getting paramater from formgroup
  }

}

