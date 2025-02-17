import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  private baseUrl = 'http://localhost:8000/api'; // Replace with your backend URL

  constructor(private http: HttpClient) { }

  getCandidateApplications(candidateId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/applications/candidate/${candidateId}`);
  }

  getCandidateInterviewStatus(candidateId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/interviews/status/${candidateId}`);
  }

  getEmployerJobPostings(employerId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/job-postings/employer/${employerId}`);
  }

  getJobApplications(jobId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/applications/job/${jobId}`);
  }

  scheduleInterview(interviewData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/interviews/schedule`, interviewData);
  }
}
