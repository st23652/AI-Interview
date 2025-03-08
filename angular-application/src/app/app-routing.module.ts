import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CandidateDashboardComponent } from './candidate-dashboard/candidate-dashboard.component'; // Adjust as necessary

const routes: Routes = [
  { path: 'dashboard', component: CandidateDashboardComponent },
  // Other routes can go here
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
