import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-photo-item',
  templateUrl: './photo-item.component.html',
  styleUrls: ['./photo-item.component.less']
})
export class PhotoItemComponent {
  @Input() public src!: string
}
