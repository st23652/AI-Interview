import { Component } from '@angular/core';
import { InterviewService } from './interview.service';

@Component({
  selector: 'app-interview',
  templateUrl: './interview.component.html',
  standalone: true,
  styleUrls: ['./interview.component.css']
})
export class InterviewComponent {
  jobRole = "Software Engineer";
  candidateAnswer = "";
  aiQuestion = "Welcome! Let's begin your interview.";
  private aiFeedback: number[] | undefined;

  constructor(private interviewService: InterviewService) {}

  submitAnswer() {
    this.interviewService.getNextQuestion(this.jobRole, this.candidateAnswer).subscribe(response => {
      this.aiQuestion = response.question;
    });

    this.interviewService.getFeedback(this.jobRole, this.aiQuestion, this.candidateAnswer).subscribe(response => {
      this.aiFeedback = response.feedback;
    });

    this.candidateAnswer = "";
  }

}
