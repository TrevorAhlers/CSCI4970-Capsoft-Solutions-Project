import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from '@services/data.service';

@Component({
	selector: 'app-conflict-manager',
	templateUrl: './conflict-manager.component.html',
	styleUrls: ['./conflict-manager.component.scss']
})
export class ConflictManagerComponent implements OnInit {
	activeConflicts: string[] = [];
	ignoredConflicts: string[] = [];

	constructor(private http: HttpClient, private dataService: DataService) {}

	ngOnInit(): void {
		this.dataService.conflictRefresh$.subscribe(() => {
			this.loadConflicts();
		});
		this.loadConflicts();
	}

	loadConflicts(): void {
		this.http.get('/conflicts/all', { responseType: 'text' }).subscribe({
			next: (data: string) => {
				try {
					const parsed = JSON.parse(data);
					if (Array.isArray(parsed)) {
						this.activeConflicts = parsed;
						this.ignoredConflicts = [];
					}
				} catch (_) {}
			}
		});
	}

	onIgnoreConflict(index: number): void {
		const ignored = this.activeConflicts.splice(index, 1)[0];
		this.ignoredConflicts.push(ignored);
	}
}
