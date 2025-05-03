import { Component, ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
	selector: 'app-registration',
	templateUrl: './registration.component.html',
	styleUrls: ['./registration.component.scss'],
	encapsulation: ViewEncapsulation.None
})
export class RegistrationComponent {
	constructor(private router: Router, private http: HttpClient) {}

	createAnAccount = new FormGroup({
		username: new FormControl('', Validators.required),
		email: new FormControl('', [Validators.required, Validators.email]),
		password: new FormControl('', Validators.required),
		confirm_password: new FormControl('', Validators.required)
	});

	createUser() {
		const f = this.createAnAccount.value;
		if (f.password !== f.confirm_password) return;

		const payload = {
			username: f.username,
			email: f.email,
			password: f.password
		};

		this.http.post(`${environment.apiBaseUrl}/api/register`, payload)
			.subscribe({
				next: () => this.router.navigateByUrl('/login'),
				error: err => console.error('Registration failed:', err)
			});
	}
}
