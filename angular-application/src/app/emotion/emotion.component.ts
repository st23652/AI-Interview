// src/app/emotion/emotion.component.ts

import { Component, OnInit, OnDestroy } from '@angular/core';
import { EmotionService } from '../emotion.service';

@Component({
  selector: 'app-emotion',
  templateUrl: './emotion.component.html',
  styleUrls: ['./emotion.component.css']
})
export class EmotionComponent implements OnInit, OnDestroy {
  emotionResult: string = '';
  videoElement: HTMLVideoElement | null = null;
  canvasElement: HTMLCanvasElement | null = null;
  canvasContext: CanvasRenderingContext2D | null = null;
  stream: MediaStream | null = null;
  frameInterval: any;

  constructor(private emotionService: EmotionService) {}

  ngOnInit(): void {
    this.videoElement = document.createElement('video');
    this.canvasElement = document.createElement('canvas');
    this.canvasContext = this.canvasElement?.getContext('2d');

    this.startVideoStream();
  }

  ngOnDestroy(): void {
    // Cleanup the webcam stream when the component is destroyed
    if (this.stream) {
      const tracks = this.stream.getTracks();
      tracks.forEach(track => track.stop());
    }
    if (this.frameInterval) {
      clearInterval(this.frameInterval);
    }
  }

  startVideoStream(): void {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        this.videoElement!.srcObject = stream;
        this.stream = stream;
        this.videoElement!.play();

        // Start capturing frames from the video feed
        this.frameInterval = setInterval(() => {
          if (this.canvasContext && this.videoElement) {
            this.canvasContext.drawImage(this.videoElement, 0, 0, 640, 480);
            this.detectEmotion();
          }
        }, 100);
      })
      .catch(err => {
        console.error('Error accessing webcam: ', err);
      });
  }

  detectEmotion(): void {
    if (!this.canvasContext || !this.canvasElement) return;
    const imageData = this.canvasContext.getImageData(0, 0, 640, 480);
    const formData = new FormData();
    formData.append('image', this.dataURLtoBlob(this.canvasElement.toDataURL()));

    this.emotionService.detectEmotion(formData).subscribe(
      (response: any) => {
        if (response.emotion) {
          this.emotionResult = `Detected Emotion: ${response.emotion}`;
        } else {
          this.emotionResult = response.error;
        }
      },
      (error) => {
        this.emotionResult = 'Error detecting emotion';
      }
    );
  }

  dataURLtoBlob(dataURL: string): Blob {
    const byteString = atob(dataURL.split(',')[1]);
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const uintArray = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
      uintArray[i] = byteString.charCodeAt(i);
    }
    return new Blob([uintArray], { type: 'image/png' });
  }
}
