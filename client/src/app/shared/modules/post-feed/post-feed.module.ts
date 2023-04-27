import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PostFeedComponent } from './post-feed.component';
import { PostModule } from '../post/post.module';



@NgModule({
  declarations: [PostFeedComponent],
  imports: [CommonModule, PostModule],
  exports: [PostFeedComponent]
})
export class PostFeedModule {}
