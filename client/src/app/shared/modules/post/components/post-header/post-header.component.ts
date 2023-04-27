import { Component } from '@angular/core';
import * as moment from 'moment';

@Component({
  selector: 'app-post-header',
  templateUrl: './post-header.component.html',
  styleUrls: ['./post-header.component.less']
})
export class PostHeaderComponent {
  profileImageSource: string =
    '../../../../../../assets/images/img-example.png';
  userFirstName: string = 'Серёжа';
  userLastName: string = 'Тенькаев';
  postCreationTime: moment.Moment = moment() 
    .set({ month: 3, date: 27, hours: 14, minutes: 38, seconds: 0 })
    .locale('ru');

  constructor() {}

  getPostTimeInfo() {
    const presentTime = moment().locale('ru');
    const diffHours = presentTime.diff(this.postCreationTime, 'hours');
    if (diffHours <= 2) {
      return this.postCreationTime.from(presentTime);
    }
    const diffYears = presentTime.diff(this.postCreationTime, 'years');
    if (diffYears) {
      return this.postCreationTime.format('ll');
    }
    const minutes = this.postCreationTime.minutes();
    const hours = this.postCreationTime.hours();
    return `${this.postCreationTime.format('DD MMM')} в ${hours}:${minutes}`;
  }
}
