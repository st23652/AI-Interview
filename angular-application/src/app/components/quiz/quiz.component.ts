import { Component, OnInit } from '@angular/core';
import { QuestionService } from '../../services/question.service';
import { Question } from '../../models/question.model';

@Component({
  selector: 'app-quiz',
  templateUrl: './quiz.component.html',
  styleUrls: ['./quiz.component.css']
})
export class QuizComponent implements OnInit {
  questions: Question[] = [];
  currentQuestionIndex = 0;
  selectedAnswer: string = '';

  constructor(private questionService: QuestionService) {}

  ngOnInit() {
    this.questionService.getQuestions().subscribe(data => {
      this.questions = data;
    });
  }

  submitAnswer() {
    if (this.selectedAnswer === this.questions[this.currentQuestionIndex].answer) {
      alert('Correct!');
    } else {
      alert('Wrong Answer!');
    }
    this.currentQuestionIndex++;
  }
}
