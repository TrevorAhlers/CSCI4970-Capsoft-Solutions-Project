import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HomeComponent } from './home.component';
import { UploadComponent } from './view/upload/upload.component';
import { ConflictManagerComponent} from './conflict-manager/conflict-manager.component';
import { FileManagerComponent} from './file-manager/file-manager.component';
import { DetailsComponent} from './details/details.component';
import { ProfileComponent} from './profile/profile.component';
import { SectionComponent } from './view/sectionview/section.component';
import { HttpClientModule } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HomeRoutingModule } from './home.routes';
import { LoginComponent } from '../login/login.component';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';


@NgModule({
	imports: [
		CommonModule,
		HttpClientModule,
		MatCardModule,
		MatButtonModule,
		MatTabsModule,
		MatDividerModule,
		MatIconModule,
		HomeRoutingModule,
		CommonModule,
		HttpClientModule,
		MatTableModule,
		MatSortModule,
		MatFormFieldModule,
		MatInputModule,

	],
	declarations: [
		HomeComponent,
		UploadComponent,
		ConflictManagerComponent,
		FileManagerComponent,
		DetailsComponent,
		ProfileComponent,
		SectionComponent
		
	
	],
	exports: [
		HomeComponent
	],
	providers: [
		provideAnimationsAsync(),
		provideAnimationsAsync('noop')
	],
	schemas: [
		CUSTOM_ELEMENTS_SCHEMA
	]
})
export class HomeModule {}
