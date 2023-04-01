import { PostComponent } from './post.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TuiButtonModule } from '@taiga-ui/core';
import { PostControlBarComponent } from './components/post-control-bar/post-control-bar.component';

@NgModule({
  declarations: [PostComponent, PostControlBarComponent],
  imports: [CommonModule, TuiButtonModule],
  exports: [PostComponent]
})
export class PostModule {}
