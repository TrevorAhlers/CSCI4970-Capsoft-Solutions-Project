import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';  
import { DataService } from './home/data.service';
import { AppComponent } from './app.component';  
import { HomeComponent } from './home/home.component';  
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component'; 
import { DataComponent } from './data/data.component';


const routes: Routes = [
  { path: '', component: LoginComponent },
  { path: 'home', component: HomeComponent },
  { path: 'data', component: DataComponent }
];

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    DataComponent  
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes),
    HttpClientModule
  ],
  bootstrap: [AppComponent]
})

export class AppModule { }