import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {
  TuiAlertModule,
  TuiDialogModule,
  TuiRootModule,
  TUI_SANITIZER
} from '@taiga-ui/core';
import { NgDompurifySanitizer } from '@tinkoff/ng-dompurify';
import { UserPageModule } from './pages/user-page/user-page.module';

import { StoreModule } from '@ngrx/store';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

@NgModule({
  declarations: [AppComponent],
  imports: [
    UserPageModule,
    BrowserModule,
    AppRoutingModule,
    StoreModule.forRoot({}, {}),
    BrowserAnimationsModule,
    TuiRootModule,
    TuiDialogModule,
    TuiAlertModule
  ],
  providers: [{ provide: TUI_SANITIZER, useClass: NgDompurifySanitizer }],
  bootstrap: [AppComponent]
})
export class AppModule {}
