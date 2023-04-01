import { PostModule } from './../../shared/modules/post/post.module';
import { UserAvatarModule } from './../../shared/modules/user-avatar/user-avatar.module';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { TuiButtonModule, TuiSvgModule } from '@taiga-ui/core';
import { TuiBadgeModule } from '@taiga-ui/kit';
import { ActionsSectionComponent } from './components/actions-section/actions-section.component';
import { FriendsSectionComponent } from './components/friends-section/friends-section.component';
import { InfoSectionComponent } from './components/info-section/info-section.component';
import { PhotosSectionComponent } from './components/photos-section/photos-section.component';
import { UserPageComponent } from './user-page.component';
import { UserPageSectionComponent } from './components/user-page-section/user-page-section.component';
import { OnlineBadgeComponent } from './components/online-badge/online-badge.component';

@NgModule({
  declarations: [
    UserPageComponent,
    InfoSectionComponent,
    ActionsSectionComponent,
    PhotosSectionComponent,
    FriendsSectionComponent,
    UserPageSectionComponent,
    OnlineBadgeComponent
  ],
  imports: [
    CommonModule,
    TuiButtonModule,
    TuiSvgModule,
    TuiBadgeModule,
    UserAvatarModule,
    PostModule
  ],
  exports: [UserPageComponent]
})
export class UserPageModule {}
