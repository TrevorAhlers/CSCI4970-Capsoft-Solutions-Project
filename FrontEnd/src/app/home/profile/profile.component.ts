import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';

@Component({
	selector: 'app-profile',
	templateUrl: './profile.component.html',
	styleUrls: ['./profile.component.scss']
})
export class ProfileComponent {
	@Input() username: string = 'Guest User';
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

downloadCsv(): void {
	const link = document.createElement('a');
	link.href = `${environment.apiBaseUrl}/api/download`;
	link.download = 'room_assignments.csv';
	link.click();
}

saveChanges(): void {
	const link = document.createElement('a')
	link.href      = `${environment.apiBaseUrl}/api/change-log`
	link.download  = 'change_log.txt'
	link.click()
}
}
