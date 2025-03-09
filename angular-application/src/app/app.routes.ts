import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
// Import your components here
import { DashboardComponent } from './dashboard/dashboard.component'; // Example component

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' }, // Redirect to home
  { path: 'dashboard', component: DashboardComponent }, // Dashboard route
  { path: '**', redirectTo: '/home' } // Redirect all other routes to home
];

@NgModule({
  imports: [RouterModule.forRoot(routes)], // Import routes
  exports: [RouterModule] // Export RouterModule
})
export class AppRoutingModule { }

export { routes }; // Ensure you export the routes
