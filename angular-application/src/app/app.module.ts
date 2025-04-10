import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app.routing.module';
import { NavbarComponent } from './components/navbar/navbar.component';
import { QuizComponent } from './components/quiz/quiz.component';
import { HomeComponent } from './pages/home/home.component';
import { QuizPageComponent } from './pages/quiz-page/quiz-page.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [BrowserModule, AppRoutingModule, HttpClientModule, QuizPageComponent, HomeComponent, QuizComponent, NavbarComponent],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {}
