import { Component } from '@angular/core';
import {QuizComponent} from "../../components/quiz/quiz.component";

@Component({
  selector: 'app-quiz-page',
  templateUrl: './quiz-page.component.html',
  imports: [
    QuizComponent
  ],
  styleUrls: ['./quiz-page.component.css']
})
export class QuizPageComponent {}
