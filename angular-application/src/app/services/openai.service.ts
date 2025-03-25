import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OpenaiService {
  private apiUrl = 'https://api.openai.com/v1/completions';
  private apiKey = 'YOUR_OPENAI_API_KEY'; // Replace with your OpenAI API key

  constructor(private http: HttpClient) {}

  generateQuestion(theme: string, numQuestions: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json'
    });

    const prompt = `Generate ${numQuestions} ${theme} questions for practice.`;
    const data = {
      model: 'text-davinci-003',  // or any other suitable model
      prompt: prompt,
      max_tokens: 500
    };

    return this.http.post<any>(this.apiUrl, data, { headers });
  }
}
