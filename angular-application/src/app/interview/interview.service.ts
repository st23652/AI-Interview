import { Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class InterviewService {
  private apiUrl = 'http://127.0.0.1:8000/api/interview/';

  constructor(private http: HttpClient) {}

  getNextQuestion(jobRole: string, previousAnswer: string): Observable<any> {
    return this.http.post(this.apiUrl, { job_role: jobRole, previous_answer: previousAnswer });
  }

  getFeedback(jobRole: string, question: string, candidateAnswer: string): Observable<any> {
    return this.http.post(this.apiUrl + "feedback/", { job_role: jobRole, question: question, candidate_answer: candidateAnswer });
  }
}
