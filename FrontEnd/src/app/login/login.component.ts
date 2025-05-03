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
	loginFailed = false;

	constructor(private router: Router, private http: HttpClient) {}

	loginForm = new FormGroup({
		username: new FormControl('', Validators.required),
		password: new FormControl('', Validators.required)
	});

	loginUser() {
		const { username, password } = this.loginForm.value as any;

		this.http.post<{ token: string }>(`${environment.apiBaseUrl}/api/login`, { username, password })
			.subscribe({
				next: res => {
					this.loginFailed = false;
					localStorage.setItem('jwt', res.token);
					this.router.navigateByUrl('/home');
				},
				error: () => {
					this.loginFailed = true;
				}
			});
	}

	navigateToRegistration() {
		this.router.navigateByUrl('/registration');
	}
}
