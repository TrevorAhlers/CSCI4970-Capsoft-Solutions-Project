import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { HomeRoutingModule } from './home.routes';

import { HomeComponent } from './home.component';
import { UploadComponent } from './view/upload/upload.component';
import { ConflictManagerComponent } from './conflict-manager/conflict-manager.component';
import { FileManagerComponent } from './file-manager/file-manager.component';
import { DetailsComponent } from './details/details.component';
import { ProfileComponent } from './profile/profile.component';
import { SectionComponent } from './view/sectionview/section.component';
import { SectionRowComponent } from './view/sectionview/section-row.component';
import { ClassComponent } from './view/classroomview/classroom.component';
import { ConflictCardComponent } from './conflict-manager/conflict-card.component';
import { ColumnSelectorDialogComponent } from './view/sectionview/column-selector-dialog.component';
import { AssignmentLogicDialogComponent } from './view/upload/assignment-logic-dialog.component';
import { TrainingDataDialogComponent } from './view/upload/training-data-dialog.component';

/* ───────────────────  Angular Material ─────────────────── */
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialogModule } from '@angular/material/dialog';

@NgModule({
	imports: [
		CommonModule,
		FormsModule,
		HttpClientModule,
		HomeRoutingModule,

		/* Material */
		MatCardModule,
		MatButtonModule,
		MatTabsModule,
		MatDividerModule,
		MatIconModule,
		MatTableModule,
		MatSortModule,
		MatFormFieldModule,
		MatInputModule,
		MatCheckboxModule,
		MatProgressSpinnerModule,
		MatDialogModule
	],
	declarations: [
		HomeComponent,
		UploadComponent,
		ConflictManagerComponent,
		FileManagerComponent,
		DetailsComponent,
		ProfileComponent,
		SectionComponent,
		SectionRowComponent,
		ClassComponent,
		ConflictCardComponent,
		ColumnSelectorDialogComponent,
		AssignmentLogicDialogComponent,
		TrainingDataDialogComponent
	],
	exports: [
		HomeComponent
	],
	providers: [],
	schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class HomeModule {}
