import { Component, Input } from '@angular/core';
import { Group } from '../../../../types/models/groupModel';

@Component({
  selector: 'app-groups-section',
  templateUrl: './groups-section.component.html',
  styleUrls: ['./groups-section.component.less']
})
export class GroupsSectionComponent {
  @Input() public firstGroups!: Group[]
  @Input() public groupsCount!: number

}
