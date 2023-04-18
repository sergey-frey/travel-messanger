import { Component } from '@angular/core';

@Component({
  selector: 'app-post-images',
  templateUrl: './post-images.component.html',
  styleUrls: ['./post-images.component.less']
})
export class PostImagesComponent {
  imageSources: string[] = [
    'https://fakeimg.pl/300x400/?text=Hello',
    'https://fakeimg.pl/800x300/?text=Bay'
  ];
  index = 0;

  public prevImage() {
    this.index =
      (this.index + this.imageSources.length - 1) % this.imageSources.length;
  }

  public nextImage() {
    this.index = (this.index + 1) % this.imageSources.length;
  }
}
