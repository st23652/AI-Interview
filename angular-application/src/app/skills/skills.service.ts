import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class SkillsService {
  constructor(private http: HttpClient) {}

  getQuestions(theme: string, numQuestions: number): Observable<any> {
    return this.http.get<any>(`http://localhost:8000/api/skills-questions/?theme=${theme}&num_questions=${numQuestions}`);
  }
}
