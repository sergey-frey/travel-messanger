import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-online-badge',
  templateUrl: './online-badge.component.html',
  styleUrls: ['./online-badge.component.less']
})
export class OnlineBadgeComponent {
  @Input() public isOnline!: boolean;
}
