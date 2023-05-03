import { Component, Input } from '@angular/core';
import { Friend } from '../../../../types/models/friendModel';

@Component({
  selector: 'app-friends-section',
  templateUrl: './friends-section.component.html',
  styleUrls: ['./friends-section.component.less']
})
export class FriendsSectionComponent {
  @Input() public friendsCount!: number
  @Input() public onlineFriendsCount!: number
  @Input() public firstFriends!: Friend[]
  @Input() public firstOnlineFriends!: Friend[]
  constructor() {

  }
  ngOnInit() {
    if (this.onlineFriendsCount) {
      this.firstFriends = this.firstFriends.slice(0, 4)
    }
  }
}
