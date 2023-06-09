import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-friend-item',
  templateUrl: './friend-item.component.html',
  styleUrls: ['./friend-item.component.less']
})
export class FriendItemComponent {
  @Input() public src!: string
  @Input() public name!: string
}
