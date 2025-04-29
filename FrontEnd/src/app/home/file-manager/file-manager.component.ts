import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from '@services/data.service';
import { environment } from 'src/environments/environment';

interface StoredFile {
	id: number;
	filename: string;
}

@Component({
	selector: 'app-file-manager',
	templateUrl: './file-manager.component.html',
	styleUrls: ['./file-manager.component.scss']
})
export class FileManagerComponent implements OnInit {

	files:       StoredFile[] = [];
	selectedId:  number|null = null;
	private readonly API = environment.apiBaseUrl;

	constructor(
		private http: HttpClient,
		private dataService: DataService
	) {}

	ngOnInit(): void {
		this.refreshList();
	}

	private refreshList(): void {
		this.http.get<StoredFile[]>(`${this.API}/assignment-files`)
			.subscribe(r => this.files = r ?? []);
	}

	loadFile(id: number): void {
		if (id === this.selectedId) return;
		this.http.get(`${this.API}/assignment-file/${id}`)
			.subscribe(() => {
				this.selectedId = id;
				this.dataService.triggerConflictRefresh();
			});
	}
}
