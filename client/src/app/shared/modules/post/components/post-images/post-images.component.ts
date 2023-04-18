import { Component } from '@angular/core';


@Component({
  selector: 'app-post-images',
  templateUrl: './post-images.component.html',
  styleUrls: ['./post-images.component.less']
})
export class PostImagesComponent {
  imageSources: string[] = ['../../../../../../assets/images/blur-example.jpg', 'https://fakeimg.pl/300x400/?text=Hello']
  index  = 0
}
