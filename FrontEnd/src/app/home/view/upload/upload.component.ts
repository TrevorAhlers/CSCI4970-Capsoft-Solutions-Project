import { Component, Output, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from '@services/data.service';
import { environment } from 'src/environments/environment';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent {
  @Output() fileUploaded = new EventEmitter<void>();
  loading = false;

  constructor(private http: HttpClient, private dataService: DataService) {}

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (!file) { return; }

    const formData = new FormData();
    formData.append('file', file, file.name);

    this.loading = true;
    this.http.post(
        `${environment.apiBaseUrl}/upload`,
        formData
      ).pipe(
        finalize(() => this.loading = false)
      )
      .subscribe({
        next: () => {
          this.dataService.triggerRefresh();
          this.dataService.triggerConflictRefresh();
          this.fileUploaded.emit();
        },
        error: err => {
          console.error('Error uploading file:', err);
        }
      });
  }
}
