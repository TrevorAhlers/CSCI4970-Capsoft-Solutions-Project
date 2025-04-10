import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
	selector: 'app-conflict-manager',
	templateUrl: './conflict-manager.component.html',
	styleUrls: ['./conflict-manager.component.scss']
})
export class ConflictManagerComponent implements OnInit {
	activeConflicts: string[] = [];
	ignoredConflicts: string[] = [];

	constructor(private http: HttpClient) {}

	ngOnInit(): void {
		console.log('[conflict-manager] ngOnInit fired');
	
		this.http.get('/conflicts/all', { responseType: 'text' }).subscribe({
			next: (data: string) => {
				console.log('[conflict-manager] 🔥 RAW RESPONSE:', data);
	
				try {
					const parsed = JSON.parse(data);
					if (Array.isArray(parsed)) {
						this.activeConflicts = parsed;
						console.log('[conflict-manager] Parsed conflicts:', this.activeConflicts);
					} else {
						console.error('[conflict-manager] Not an array:', parsed);
					}
				} catch (e) {
					console.error('[conflict-manager] JSON parse error:', e);
				}
			},
			error: (err) => {
				console.error('[conflict-manager] HTTP error:', err);
			}
		});
	}
	
	

	onIgnoreConflict(index: number): void {
		const ignored = this.activeConflicts.splice(index, 1)[0];
		this.ignoredConflicts.push(ignored);
		console.log(`[conflict-manager] Ignored conflict ${index}`);
	}
}
