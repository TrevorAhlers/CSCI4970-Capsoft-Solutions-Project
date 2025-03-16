import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';  
import { DataService } from './home/data.service';
import { AppComponent } from './app.component';  
import { HomeComponent } from './home/home.component';  
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async'; 
import { MatCard } from '@angular/material/card';
import { MatCardModule } from '@angular/material/card';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import {MDCRipple} from '@material/ripple';
import { MatButtonModule } from '@angular/material/button';
import {MatTabsModule} from '@angular/material/tabs';
import {MatDividerModule} from '@angular/material/divider'
import {MatIconModule} from '@angular/material/icon';
const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'home', component: HomeComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent  
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes),
    HttpClientModule,
    MatCardModule,
    MatCard,
    MatButtonModule,
    MatTabsModule,
    MatDividerModule,
    MatIconModule
    
  ],
  bootstrap: [AppComponent],
  providers: [
    provideAnimationsAsync()
  ],
  schemas: [
    CUSTOM_ELEMENTS_SCHEMA // Add this line
  ]

})

export class AppModule { }