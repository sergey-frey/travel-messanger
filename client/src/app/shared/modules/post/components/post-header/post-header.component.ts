import { Component, Input } from '@angular/core';
import * as moment from 'moment';

@Component({
  selector: 'app-post-header',
  templateUrl: './post-header.component.html',
  styleUrls: ['./post-header.component.less']
})
export class PostHeaderComponent {
  @Input() public authorImg!: string
  @Input() public  authorFName!: string
  @Input() public  authorLName!: string
  @Input() public date!: moment.Moment

  constructor() {}

  getPostTimeInfo() {
    const presentTime = moment().locale('ru');
    const diffHours = presentTime.diff(this.date, 'hours');
    if (diffHours <= 2) {
      return this.date.from(presentTime);
    }
    const diffYears = presentTime.diff(this.date, 'years');
    if (diffYears) {
      return this.date.format('ll');
    }
    const minutes = this.date.minutes();
    const hours = this.date.hours();
    return `${this.date.format('DD MMM')} в ${hours}:${minutes}`;
  }
}
