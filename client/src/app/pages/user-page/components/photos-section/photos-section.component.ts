import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-photos-section',
  templateUrl: './photos-section.component.html',
  styleUrls: ['./photos-section.component.less']
})
export class PhotosSectionComponent {
  @Input() images!: string[]
  firstImages: string[] = []
  ngOnInit() {
    this.firstImages = this.images.slice(0, 4)
  }
}
