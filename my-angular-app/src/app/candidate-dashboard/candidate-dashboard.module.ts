import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CandidateDashboardComponent } from './candidate-dashboard.component';

@NgModule({
  declarations: [
    CandidateDashboardComponent
  ],
  imports: [
    CommonModule // Make sure this is imported
  ],
  exports: [
    CandidateDashboardComponent
  ]
})
export class CandidateDashboardModule { }
