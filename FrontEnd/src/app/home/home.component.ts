import { Component, OnInit } from '@angular/core';
import { DataService } from '@services/data.service';
import { Router } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import {MatTabsModule} from '@angular/material/tabs';
import {MatDividerModule} from '@angular/material/divider'
import { HttpClient } from '@angular/common/http';




@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss'],
    standalone: false
})
export class HomeComponent {

 
  profileImage:string = "Capture.png"

}

      
  
