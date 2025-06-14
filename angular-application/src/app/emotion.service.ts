// src/app/emotion.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EmotionService {

  private apiUrl = '/api/process_image/';  // Your Django endpoint

  constructor(private http: HttpClient) {}

  detectEmotion(imageData: FormData): Observable<any> {
    return this.http.post(this.apiUrl, imageData);
  }
}
