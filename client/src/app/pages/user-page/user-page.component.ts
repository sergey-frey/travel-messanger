import { Component } from '@angular/core';

@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.less']
})
export class UserPageComponent {
  images: string[] = new Array(20).fill('../../../assets/images/img-example.png')
  avatar: string = '../../../assets/aa1b8ce6570e33aa6b0bc0c475f2895e.jpg'
}
