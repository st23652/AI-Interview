import { Component } from '@angular/core';
import { OpenaiService } from '../services/openai.service';

@Component({
  selector: 'app-quiz',
  templateUrl: './quiz.component.html',
  styleUrls: ['./quiz.component.css']
})
export class QuizComponent {
  theme: string = 'swe';
  numQuestions: number = 5;
  questions: any[] = [];
  currentQuestionIndex: number = 0;
  answerFeedback: string = '';

  constructor(private openaiService: OpenaiService) {}

  startQuiz() {
    this.openaiService.generateQuestion(this.theme, this.numQuestions).subscribe(
      (data) => {
        this.questions = data.choices[0].text.split('\n').map((text: string) => ({ question: text }));
        this.currentQuestionIndex = 0;
        this.answerFeedback = '';
      },
      (error) => {
        console.error('Error generating questions:', error);
      }
    );
  }

  nextQuestion(answer: string) {
    const correctAnswer = 'correct-answer'; // Ideally, you would generate this based on the questions or have a backend API for it
    this.answerFeedback = answer === correctAnswer ? 'Correct!' : 'Incorrect!';
    this.currentQuestionIndex++;

    if (this.currentQuestionIndex >= this.questions.length) {
      this.answerFeedback = 'Quiz Completed!';
    }
  }

  onThemeChange(event: any) {
    this.theme = event.target.value;
  }

  onNumQuestionsChange(event: any) {
    this.numQuestions = event.target.value;
  }
}
