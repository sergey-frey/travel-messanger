import { Component, Input } from '@angular/core';
import { Friend } from '../../../../types/models/friendModel';

@Component({
  selector: 'app-friends-section',
  templateUrl: './friends-section.component.html',
  styleUrls: ['./friends-section.component.less']
})
export class FriendsSectionComponent {
  // friends: object[] = [{},{}, {}, {}, {}, {}, {}, {}, {}, {}]
  // onlineFriends: object[] = [{},{}, {}, {}, {}]

  // friendsCount: number = this.friends.length
  // onlineFriendsCount: number = this.onlineFriends.length
  // firstFriends: object[] = this.friends.slice(0, 4)
  // firstOnlineFriends: object[] = this.onlineFriends.slice(0, 4)

  @Input() friendsCount!: number
  @Input() onlineFriendsCount!: number
  @Input() firstFriends!: Friend[]
  @Input() firstOnlineFriends!: Friend[]
  constructor() {

  }
  ngOnInit() {
    if (this.onlineFriendsCount) {
      this.firstFriends = this.firstFriends.slice(0, 4)
    }
  }
}
