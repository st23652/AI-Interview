import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SkillsComponent } from './skills.component';
import { SkillsRoutingModule } from './skills-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
// @ts-ignore
import { ChartsModule } from 'ng2-charts';

@NgModule({
  declarations: [],
  imports: [CommonModule, SkillsRoutingModule, HttpClientModule, FormsModule, ChartsModule, SkillsComponent],
})
export class SkillsModule {}
