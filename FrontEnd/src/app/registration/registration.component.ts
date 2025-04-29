import { Component, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
<<<<<<< HEAD
import { FormControl, FormGroup } from '@angular/forms';
import { Validators } from "@angular/forms";
=======
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
>>>>>>> dev-tyler

@Component({
	selector: 'app-registration',
	templateUrl: './registration.component.html',
	styleUrls: ['./registration.component.scss'],
	encapsulation: ViewEncapsulation.None
})
export class RegistrationComponent {
<<<<<<< HEAD
    constructor(private router: Router) {}
    createAnAccount = new FormGroup({
        username: new FormControl('',
          [Validators.required,
          Validators.minLength(5),]
        ),
        email:new FormControl('',[Validators.required,this.emailPatternCheck]),
        password: new FormControl('',[Validators.required,  this.passwordPatternCheck]),
        confirm_password: new FormControl('',[Validators.required])
      })

      regex_pattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/

      emailPattern = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}/i;

    createAccount(){
      if (this.createAnAccount.valid) {
        this.router.navigateByUrl('/login');
      } 
    }

    
    passwordPatternCheck(control: FormControl): { [key: string]:boolean} |null{
      const nonWhitespaceRegExp: RegExp = new RegExp('/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/');
      if (control.value && !nonWhitespaceRegExp.test(control.value)) {
        return {'passwordPatternCheck': true};
      }
      return null;
    }
    

    emailPatternCheck(control: FormControl): { [key: string]: boolean } | null {
      const emailPattern: RegExp = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,6}/i;
      if (control.value && !emailPattern.test(control.value)) {
        return { 'emailPatternCheck': true };
      }
      return null;
    }

    emailCustomErrorMsg(): string | null{
      const passwordControl = this.createAnAccount.get('email');
      if (passwordControl?.hasError('emailPatternCheck')) {
        return 'Invalid Email Pattern';
        
      } 
      return null;
    }

    passwordCustomErrorMessages(): string | null{
      const passwordControl = this.createAnAccount.get('password');
      if (passwordControl?.hasError('passwordPatternCheck')) {
        return 'The given password doesn"t match requirement of at least 8 characters long and contains only letters and digits.';
        
      } 
      return null;
    }

    passwordCustomErrorMessages2(): string | null{
      const passwordControl = this.createAnAccount.get('password');
      if (passwordControl?.hasError('heckNoBlankSpaces')) {
        return 'The given password doesn"t match requirement of at least 8 characters long and contains only letters and digits.';
        
      } 
      return null;
    }



   
}
=======
	constructor(private router: Router, private http: HttpClient) {}

	createAnAccount = new FormGroup({
		username: new FormControl('', Validators.required),
		email:    new FormControl('', [Validators.required, Validators.email]),
		password: new FormControl('', Validators.required),
		confirm_password: new FormControl('', Validators.required)
	});

	createUser() {
		const f = this.createAnAccount.value;
		if (f.password !== f.confirm_password) return;

		const payload = {
			username: f.username,
			email:    f.email,
			password: f.password
		};

		this.http.post(`${environment.apiBaseUrl}/api/register`, payload)
			.subscribe({
				next: () => this.router.navigateByUrl('/login'),
				error: err => console.error('Registration failed:', err)
			});
	}
}
>>>>>>> dev-tyler
