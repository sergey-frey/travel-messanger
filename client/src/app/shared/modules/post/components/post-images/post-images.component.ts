import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-post-images',
  templateUrl: './post-images.component.html',
  styleUrls: ['./post-images.component.less']
})
export class PostImagesComponent {
  @Input() public photos!: string[]
  index = 0;

  public prevImage() {
    this.index =
      (this.index + this.photos.length - 1) % this.photos.length;
  }

  public nextImage() {
    this.index = (this.index + 1) % this.photos.length;
  }
}
