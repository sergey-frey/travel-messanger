import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-post-text',
  templateUrl: './post-text.component.html',
  styleUrls: ['./post-text.component.less']
})
export class PostTextComponent {
  @Input() public text!: string
  restText!: string
  needMore: boolean = false
  action: string = 'Показать ещё'

  ngOnInit() {
    if (this.text.length > 200) {
      this.needMore = true
      this.restText = this.text.slice(200)
      this.text = this.text.slice(0, 200)
    }
  }
  showMore() {
      this.needMore = !this.needMore
      if (this.needMore) {
        this.text = this.text.slice(0, 200)
        this.action = 'Показать ещё'
      } else {
        this.text += this.restText
        this.action = 'Скрыть'
      }
  }
}
