import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HomeComponent } from './home.component';
import { UploadBoxComponent } from './view/upload-box/upload-box.component';
import { ConflictManagerComponent} from './conflict-manager/conflict-manager.component';
import { FileManagerComponent} from './file-manager/file-manager.component';
import { DetailsComponent} from './details/details.component';
import { ProfileComponent} from './profile/profile.component';

import { HttpClientModule } from '@angular/common/http';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HomeRoutingModule } from './home.routes';

@NgModule({
	imports: [
		CommonModule,
		HttpClientModule,
		MatCardModule,
		MatButtonModule,
		MatTabsModule,
		MatDividerModule,
		MatIconModule,
		HomeRoutingModule
	],
	declarations: [
		HomeComponent,
		UploadBoxComponent,
		ConflictManagerComponent,
		FileManagerComponent,
		DetailsComponent,
		ProfileComponent
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
