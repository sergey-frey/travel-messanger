import { Component } from '@angular/core';

@Component({
  selector: 'app-post-feed',
  templateUrl: './post-feed.component.html',
  styleUrls: ['./post-feed.component.less']
})
export class PostFeedComponent {
  posts: Object[] = [{}, {}, {}];
}
