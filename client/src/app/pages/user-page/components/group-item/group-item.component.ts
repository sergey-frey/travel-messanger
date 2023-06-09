import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-group-item',
  templateUrl: './group-item.component.html',
  styleUrls: ['./group-item.component.less']
})
export class GroupItemComponent {
  @Input() public src!: string
  @Input() public name!: string
}
