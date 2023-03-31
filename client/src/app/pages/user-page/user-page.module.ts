import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserPageComponent } from './user-page.component';
import { InfoSectionComponent } from './components/info-section/info-section.component';
import { ActionsSectionComponent } from './components/actions-section/actions-section.component';
import { PhotosSectionComponent } from './components/photos-section/photos-section.component';
import { FriendsSectionComponent } from './components/friends-section/friends-section.component';

@NgModule({
  declarations: [
    UserPageComponent,
    InfoSectionComponent,
    ActionsSectionComponent,
    PhotosSectionComponent,
    FriendsSectionComponent
  ],
  imports: [CommonModule]
})
export class UserPageModule {}
