import { Component } from '@angular/core';
import { DashboardComponent } from './dashboard/dashboard.component';
import {RouterOutlet} from "@angular/router"; // import the standalone component

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  standalone: true,
  imports: [
    RouterOutlet
  ], // Use the imports array for standalone components
})
export class AppComponent {
    title(title: any) {
        throw new Error('Method not implemented.');
    }
}
