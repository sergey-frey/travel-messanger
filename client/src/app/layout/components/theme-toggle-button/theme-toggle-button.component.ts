import { Component } from '@angular/core';

@Component({
  selector: 'app-theme-toggle-button',
  templateUrl: './theme-toggle-button.component.html',
  styleUrls: ['./theme-toggle-button.component.less']
})
export class ThemeToggleButtonComponent {
  isDarkTheme: boolean = false;

  public toggleTheme(): void {
    this.isDarkTheme = !this.isDarkTheme;
  }
}
