import { Component } from '@angular/core';

@Component({
  selector: 'app-friends-section',
  templateUrl: './friends-section.component.html',
  styleUrls: ['./friends-section.component.less']
})
export class FriendsSectionComponent {
  friends: object[] = [{},{}, {}, {}, {}, {}, {}, {}, {}, {}, {},{}, {}, {}, {}, {}, {}, {}, {}, {}]
  onlineFriends: object[] = [{},{}, {}, {}, {}, {}, {}, {}, {}, {}]
  friendsCount: number = this.friends.length
  onlineFriendsCount: number = this.onlineFriends.length
  firstFriends: object[] = this.friends.slice(0, 4)
  firstOnlineFriends: object[] = this.onlineFriends.slice(0, 4)
}
