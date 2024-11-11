import { Component } from '@angular/core';
import { DashboardComponent } from './dashboard/dashboard.component'; // import the standalone component

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: true,
  imports: [DashboardComponent], // Use the imports array for standalone components
})
export class AppComponent { }
