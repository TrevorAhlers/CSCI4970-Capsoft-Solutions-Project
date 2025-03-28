import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
	selector: 'app-login',
	templateUrl: './login.component.html',
	styleUrls: ['./login.component.scss']
})
export class LoginComponent {
	username: string = '';
	password: string = '';

	constructor(private router: Router, private http: HttpClient) {}

	onLogin() {
		this.http.post<any>('http://localhost:5000/login', { 
			username: this.username, 
			password: this.password 
		}).subscribe({
			next: (res) => {
				localStorage.setItem('access_token', res.access_token);
				this.router.navigateByUrl('/home');
			},
			error: (err) => {
				alert('Login failed');
			}
		});
	}
}