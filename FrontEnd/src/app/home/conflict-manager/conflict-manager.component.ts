import { Component, Input, OnChanges, OnInit, OnDestroy, SimpleChanges } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from '@services/data.service';
import { Subscription } from 'rxjs';
import { environment } from 'src/environments/environment';

interface ConflictView {
	id: string;
	content: string;
	ignored: boolean;
}

@Component({
	selector: 'app-conflict-manager',
	templateUrl: './conflict-manager.component.html',
	styleUrls: ['./conflict-manager.component.scss']
})
export class ConflictManagerComponent implements OnInit, OnChanges, OnDestroy {
	@Input() clear = false;

	tab = 0;
	activeConflicts: ConflictView[] = [];
	ignoredConflicts: ConflictView[] = [];
	private activeLoaded = false;
	private ignoredLoaded = false;

	private refreshSub!: Subscription;
	private readonly API = environment.apiBaseUrl;

	constructor(private http: HttpClient, private dataService: DataService) {}

	ngOnInit(): void {
		this.refreshSub = this.dataService.conflictRefresh$.subscribe(() => {
			this.reloadBoth();
		});

		this.loadActiveConflicts();
		this.loadIgnoredConflicts();
	}

	ngOnDestroy(): void {
		if (this.refreshSub) this.refreshSub.unsubscribe();
	}

	ngOnChanges(changes: SimpleChanges): void {
		if (!changes['clear']) return;

		const { previousValue: prev, currentValue: curr } = changes['clear'];
		if (curr === true) {
			this.activeConflicts = [];
			this.ignoredConflicts = [];
			this.activeLoaded = false;
			this.ignoredLoaded = false;
			return;
		}
		if (prev === true && curr === false) this.reloadBoth();
	}

	private loadActiveConflicts(): void {
		if (this.clear || this.activeLoaded) return;
		this.http.get<ConflictView[]>(`${this.API}/conflicts/active`)
			.subscribe(r => {
				this.activeConflicts = r ?? [];
				this.activeLoaded = true;
			});
	}

	private loadIgnoredConflicts(): void {
		if (this.clear || this.ignoredLoaded) return;
		this.http.get<ConflictView[]>(`${this.API}/conflicts/ignored`)
			.subscribe(r => {
				this.ignoredConflicts = r ?? [];
				this.ignoredLoaded = true;
			});
	}

	private reloadBoth(): void {
		this.activeLoaded = false;
		this.ignoredLoaded = false;
		this.loadActiveConflicts();
		this.loadIgnoredConflicts();
	}

	onIgnoreConflict(id: string): void {
		this.http.put(`${this.API}/conflict/ignore/${id}`, {})
			.subscribe(() => this.reloadBoth());
	}

	onRestoreConflict(id: string): void {
		this.http.put(`${this.API}/conflict/activate/${id}`, {})
			.subscribe(() => this.reloadBoth());
	}

	switchTab(next: number): void {
		this.tab = next;
		if (next === 0) this.loadActiveConflicts();
		else this.loadIgnoredConflicts();
	}
}
