import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../services/dashboard.service';

@Component({
  selector: 'app-employer-dashboard',
  templateUrl: './employer-dashboard.component.html',
  styleUrls: ['./employer-dashboard.component.css']
})
export class EmployerDashboardComponent implements OnInit {

  jobPostings: any[] = [];
  selectedJobId: number | null = null;
  jobApplications: any[] = [];
  employerId = 1;  // Replace with actual employer ID

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.loadJobPostings();
  }

  loadJobPostings(): void {
    this.dashboardService.getEmployerJobPostings(this.employerId).subscribe(data => {
      this.jobPostings = data;
    });
  }

  loadJobApplications(jobId: number): void {
    this.selectedJobId = jobId;
    this.dashboardService.getJobApplications(jobId).subscribe(data => {
      this.jobApplications = data;
    });
  }

  scheduleInterview(candidateId: number): void {
    const interviewData = {
      candidateId: candidateId,
      jobId: this.selectedJobId,
      date: new Date() // Set the date dynamically
    };
    this.dashboardService.scheduleInterview(interviewData).subscribe(response => {
      console.log('Interview scheduled', response);
    });
  }
}
