import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from '@services/data.service';

interface ConflictView {
  id: string;
  content: string;
  ignored: boolean;
}

@Component({
  selector   : 'app-conflict-manager',
  templateUrl: './conflict-manager.component.html',
  styleUrls  : ['./conflict-manager.component.scss']
})
export class ConflictManagerComponent implements OnInit, OnChanges {

  /* -------- inputs & local state ---------------------------------------- */
  @Input() clear = false;
  tab = 0;                                   // 0 = active, 1 = ignored

  activeConflicts:  ConflictView[] = [];
  ignoredConflicts: ConflictView[] = [];

  private activeLoaded  = false;
  private ignoredLoaded = false;

  constructor(
    private http : HttpClient,
    private dataService: DataService
  ) {}

  /* -------- life‑cycle --------------------------------------------------- */
  ngOnInit(): void {
    this.loadActiveConflicts();
    this.loadIgnoredConflicts();

    this.dataService.conflictRefresh$.subscribe(() => {
      this.reloadBoth();
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!changes['clear']) { return; }

    const { previousValue: prev, currentValue: curr } = changes['clear'];

    if (curr === true) {                       // wiped by parent
      this.activeConflicts  = [];
      this.ignoredConflicts = [];
      this.activeLoaded  = false;
      this.ignoredLoaded = false;
      return;
    }
    if (prev === true && curr === false) {     // restore
      this.reloadBoth();
    }
  }

  /* -------- REST helpers ------------------------------------------------- */
  private loadActiveConflicts(): void {
    if (this.clear || this.activeLoaded) { return; }

    this.http.get<ConflictView[]>('/conflicts/active')
      .subscribe(r => {
        this.activeConflicts = r ?? [];
        this.activeLoaded = true;
      });
  }

  private loadIgnoredConflicts(): void {
    if (this.clear || this.ignoredLoaded) { return; }

    this.http.get<ConflictView[]>('/conflicts/ignored')
      .subscribe(r => {
        this.ignoredConflicts = r ?? [];
        this.ignoredLoaded = true;
      });
  }

  private reloadBoth(): void {
    this.activeLoaded  = false;
    this.ignoredLoaded = false;
    this.loadActiveConflicts();
    this.loadIgnoredConflicts();
  }

  /* -------- card actions ------------------------------------------------- */
  onIgnoreConflict(id: string): void {
    this.http.get(`/conflict/ignore/${id}`).subscribe(() => this.reloadBoth());
  }

  onRestoreConflict(id: string): void {
    this.http.get(`/conflict/activate/${id}`).subscribe(() => this.reloadBoth());
  }

  /* -------- manual “tab” switching -------------------------------------- */
  switchTab(target: number) {
    this.tab = target;
    if (this.tab === 0) { this.loadActiveConflicts(); }
    else                { this.loadIgnoredConflicts(); }
  }
}
