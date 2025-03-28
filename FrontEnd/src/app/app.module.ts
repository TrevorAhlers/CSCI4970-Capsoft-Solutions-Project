import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { DataComponent } from './services/data.component';
import { LoginComponent } from './login/login.component';

import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';

import { AuthInterceptor } from './interceptors/auth.interceptor';
// for login page data entry:
import { FormsModule } from '@angular/forms';

const routes: Routes = [
	{ path: '', component: LoginComponent },
	{ path: 'home', loadChildren: () => import('./home/home.module').then(m => m.HomeModule) },
	{ path: 'data', component: DataComponent }
];

@NgModule({
	declarations: [
		AppComponent,
		DataComponent,
		LoginComponent
	],
	imports: [
		BrowserModule,
		FormsModule,
		BrowserAnimationsModule,
		HttpClientModule,
		RouterModule.forRoot(routes),
		MatCardModule,
		MatButtonModule,
		MatTabsModule,
		MatDividerModule,
		MatIconModule
	],
	providers: [
		{
			provide: HTTP_INTERCEPTORS,
			useClass: AuthInterceptor,
			multi: true
		}
	],
	bootstrap: [AppComponent]
})
export class AppModule {}
