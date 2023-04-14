import { PostComponent } from './post.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TuiButtonModule } from '@taiga-ui/core';
import { PostControlBarComponent } from './components/post-control-bar/post-control-bar.component';
import { PostImagesComponent } from './components/post-images/post-images.component';

@NgModule({
  declarations: [PostComponent, PostControlBarComponent, PostImagesComponent],
  imports: [CommonModule, TuiButtonModule],
  exports: [PostComponent]
})
export class PostModule {}
