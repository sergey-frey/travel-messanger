import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-info-section',
  templateUrl: './info-section.component.html',
  styleUrls: ['./info-section.component.less']
})
export class InfoSectionComponent {
  @Input() public avatar!: string
  @Input() public firstName!: string
  @Input() public lastName!: string
  @Input() public isOnline!: boolean
  @Input() public city!: string
}
