import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component'; // Assuming this is a standalone component
import { DashboardComponent } from './dashboard/dashboard.component'; // Assuming this is a standalone component

@NgModule({
  imports: [
    BrowserModule,
    AppRoutingModule,
    // Do not declare standalone components here
  ]
})
export class AppModule { }
