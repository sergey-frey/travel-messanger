import { Component } from '@angular/core';
import { IFriend } from '../../types/models/friendModel';
import { IGroup } from '../../types/models/groupModel';
import { IPost } from '@customTypes/models';
import * as moment from 'moment';

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.less']
})
export class UserPageComponent {
  //images-section
  images: string[] = new Array(20).fill(
    '../../../assets/images/img-example.png'
  );
  firstImages!: string[];

  //info-section
  avatar: string = '../../../assets/aa1b8ce6570e33aa6b0bc0c475f2895e.jpg';
  firstName: string = 'Дмитрий';
  lastName: string = 'Щедрин';
  isOnline: boolean = true;
  city: string = 'Санкт-Петербург';

  //friends-sectino
  friends: IFriend[] = new Array(135).fill({
    name: 'Серёжа',
    img: '../../../assets/images/img-example.png'
  });
  onlineFriends: IFriend[] = new Array(12).fill({
    name: 'Серёжа',
    img: '../../../assets/images/img-example.png'
  });
  friendsCount!: number;
  onlineFriendsCount!: number;
  firstFriends!: IFriend[];
  firstOnlineFriends!: IFriend[];

  //gifts-section
  gifts: string[] = new Array(98).fill(
    '../../../assets/images/img-example.png'
  );
  giftsCount!: number;
  firstGifts!: string[];

  //groups-section
  groups: IGroup[] = new Array(87).fill({
    name: 'Web Development',
    img: '../../../assets/images/img-example.png'
  });
  groupsCount!: number;
  firstGroups!: IGroup[];

  //post-feed
  posts: IPost[] = new Array(15).fill({
    authorImg: '../../../assets/images/img-example.png',
    authorFName: 'Серёжа',
    authorLName: 'Тенькаев',
    // photos: new Array(4).fill('https://fakeimg.pl/350x420/?text=Hello'),
    photos:[ 'https://fakeimg.pl/350x420/?text=Hello', '../../../assets/images/img-example.png'],
    text: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat mollitia possimus laborum ex non eaque corporis tempora recusandae ipsa voluptatem modi iure totam at nostrum quidem, odio assumenda doloribus illum. Voluptate veniam recusandae cupiditate nam debitis soluta pariatur eligendi quos animi obcaecati at voluptatibus illo, suscipit sapiente laudantium cumque dolorum!',
    date: moment()
      .set({ month: 4, date: 3, hours: 16, minutes: 38, seconds: 0 })
      .locale('ru')
  });

  constructor() {
    this.firstImages = this.images.slice(0, 3);

    this.friendsCount = this.friends.length;
    this.onlineFriendsCount = this.onlineFriends.length;
    this.firstFriends = this.friends.slice(0, 8);
    this.firstOnlineFriends = this.onlineFriends.slice(0, 4);

    this.giftsCount = this.gifts.length;
    this.firstGifts = this.gifts.slice(0, 4);

    this.groupsCount = this.groups.length;
    this.firstGroups = this.groups.slice(0, 4);
  }
}
