import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-image-item',
  templateUrl: './image-item.component.html',
  styleUrls: ['./image-item.component.less']
})
export class ImageItemComponent {
  @Input() src!: string
}
