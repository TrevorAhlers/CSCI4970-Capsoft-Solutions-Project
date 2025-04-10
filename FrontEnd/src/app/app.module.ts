import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';  
import { DataComponent } from './services/data.component';
import { AppComponent } from './app.component';  

import { RouterModule, Routes } from '@angular/router';
import { AppRoutingModule } from './app.routes';

import { LoginComponent } from './login/login.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async'; 
import { MatCard } from '@angular/material/card';
import { MatCardModule } from '@angular/material/card';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDividerModule } from '@angular/material/divider';
import { MatIconModule } from '@angular/material/icon';
import {MatFormField} from '@angular/material/form-field'
import { MatCardTitle } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule,ReactiveFormsModule  } from '@angular/forms';
import { RegistrationComponent } from './registration/registration.component';

const routes: Routes = [
	{ path: '', component: LoginComponent },
	{ path: 'home', loadChildren: () => import('./home/home.module').then(m => m.HomeModule) },
	{ path: 'data', component: DataComponent },
	{path: 'registration', component: RegistrationComponent}
];

@NgModule({
	declarations: [
		AppComponent,
		DataComponent,
		LoginComponent,
		RegistrationComponent
	],
	imports: [
		BrowserModule,
		RouterModule.forRoot(routes),
		AppRoutingModule,
		HttpClientModule,
		MatCardModule,
		MatCard,
		MatButtonModule,
		MatTabsModule,
		MatDividerModule,
		MatIconModule,
		MatFormField,
		MatCardTitle,
		MatInputModule,
		MatFormFieldModule,
		FormsModule,
		ReactiveFormsModule
	],
	exports:[RouterModule],
	bootstrap: [AppComponent],
	providers: [
		provideAnimationsAsync(),
		provideAnimationsAsync('noop')
	],
	schemas: [
		CUSTOM_ELEMENTS_SCHEMA
	]
})
export class AppModule {}
