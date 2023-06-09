import { Component, Input } from '@angular/core';
import { IGroup } from '@customTypes/models';

@Component({
  selector: 'app-groups-section',
  templateUrl: './groups-section.component.html',
  styleUrls: ['./groups-section.component.less']
})
export class GroupsSectionComponent {
  @Input() public firstGroups!: IGroup[]
  @Input() public groupsCount!: number

}
