import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-notification-button',
  templateUrl: './notification-button.component.html',
  styleUrls: ['./notification-button.component.less']
})
export class NotificationButtonComponent {
  @Input() noticeCount: number = 0;
}
