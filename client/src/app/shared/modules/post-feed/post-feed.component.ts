import { Component, Input } from '@angular/core';
import { IPost } from '@customTypes/models';

@Component({
  selector: 'app-post-feed',
  templateUrl: './post-feed.component.html',
  styleUrls: ['./post-feed.component.less']
})
export class PostFeedComponent {
  @Input() public posts!: IPost[]
}
