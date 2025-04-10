import { Component, OnInit } from '@angular/core';
import { SkillsService } from './skills.service';
import {BaseChartDirective} from "ng2-charts";

@Component({
  selector: 'app-skills',
  templateUrl: './skills.component.html',
  styleUrls: ['./skills.component.css'],
  imports: [
    BaseChartDirective,
    BaseChartDirective,
    BaseChartDirective
  ]
})
export class SkillsComponent implements OnInit {
  themes = ['JavaScript', 'Python', 'Django', 'Angular'];
  theme = '';
  numQuestions = 5;
  questions: any[] = [];
  currentQuestionIndex = 0;
  correctAnswers = 0;
  wrongAnswers = 0;
  selectedAnswer: string = '';
  explanation: string = '';
  quizFinished = false;

  constructor(private skillsService: SkillsService) {}

  ngOnInit() {}

  startQuiz() {
    this.skillsService.getQuestions(this.theme, this.numQuestions).subscribe((data) => {
      this.questions = data;
      this.currentQuestionIndex = 0;
      this.correctAnswers = 0;
      this.wrongAnswers = 0;
      this.quizFinished = false;
    });
  }

  checkAnswer(selectedOption: string) {
    this.selectedAnswer = selectedOption;
    if (selectedOption === this.questions[this.currentQuestionIndex].correct_answer) {
      this.correctAnswers++;
    } else {
      this.wrongAnswers++;
    }
    this.explanation = this.questions[this.currentQuestionIndex].explanation;
  }

  nextQuestion() {
    if (this.currentQuestionIndex < this.questions.length - 1) {
      this.currentQuestionIndex++;
      this.selectedAnswer = '';
      this.explanation = '';
    } else {
      this.quizFinished = true;
    }
  }
}
