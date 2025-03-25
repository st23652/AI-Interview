import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { QuizComponent } from './components/quiz.component';
import { OpenaiService } from './services/openai.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    QuizComponent
  ],
  providers: [OpenaiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
