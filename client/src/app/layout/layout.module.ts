import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import {
  TuiButtonModule, TuiTextfieldControllerModule
} from '@taiga-ui/core';
import { TuiBadgedContentModule, TuiInputModule } from '@taiga-ui/kit';
import { AvatarComponent } from './components/avatar/avatar.component';
import { HeaderComponent } from './components/header/header.component';
import { LogoComponent } from './components/logo/logo.component';
import { SearchInputComponent } from './components/search-input/search-input.component';
import { ThemeToggleButtonComponent } from './components/theme-toggle-button/theme-toggle-button.component';
import { LayoutComponent } from './layout.component';
import { NotificationButtonComponent } from './components/notification-button/notification-button.component';

@NgModule({
  declarations: [
    LayoutComponent,
    HeaderComponent,
    ThemeToggleButtonComponent,
    SearchInputComponent,
    LogoComponent,
    AvatarComponent,
    NotificationButtonComponent,

  ],
  imports: [
    CommonModule,
    TuiInputModule,
    TuiButtonModule,
    TuiTextfieldControllerModule,
    TuiBadgedContentModule
  ],
  exports: [LayoutComponent]
})
export class LayoutModule {}
