import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-gifts-section',
  templateUrl: './gifts-section.component.html',
  styleUrls: ['./gifts-section.component.less']
})
export class GiftsSectionComponent {
  @Input() public giftsCount!: number
  @Input() public firstGifts!: string[]
}
