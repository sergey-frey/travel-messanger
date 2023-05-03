import { Component, Input } from '@angular/core';
import { IPost } from '@customTypes/models';

@Component({
  selector: 'app-post',
  templateUrl: './post.component.html',
  styleUrls: ['./post.component.less']
})
export class PostComponent {
  @Input() public post!: IPost
}

