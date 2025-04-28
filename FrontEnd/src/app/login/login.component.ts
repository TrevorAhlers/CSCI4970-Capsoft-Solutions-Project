import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
	selector: 'app-login',
	templateUrl: './login.component.html',
	styleUrls: ['./login.component.scss']
})
export class LoginComponent {

	constructor(private router: Router, private http: HttpClient) {}

	loginForm = new FormGroup({
		username: new FormControl('', Validators.required),
		password: new FormControl('', Validators.required)
	});

	loginUser() {
		const { username, password } = this.loginForm.value as any;

		this.http.post<{token:string}>(`${environment.apiBaseUrl}/api/login`, { username, password })
			.subscribe({
				next: res => {
					localStorage.setItem('jwt', res.token);
					this.router.navigateByUrl('/home');
				},
				error: err => console.error('Login failed:', err)
			});
	}

	navigateToRegistration() {
		this.router.navigateByUrl('/registration');
	}
}
