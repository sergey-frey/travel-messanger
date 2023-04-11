import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-avatar',
  templateUrl: './avatar.component.html',
  styleUrls: ['./avatar.component.less']
})
export class AvatarComponent {
  @Input() src: string = 'https://fakeimg.pl/100/?text=Avatar';
}
