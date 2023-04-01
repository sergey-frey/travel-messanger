import { IUser } from './../../types/models/userModel';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserDataService {
  constructor() {}

  public getUserData(): IUser {
    return {
      id: '1',
      email: '111@gmail.com',
      password: '111',
      fname: 'Дима',
      lname: 'Щедрин',
      age: 30,
      avatar: '/assets/aa1b8ce6570e33aa6b0bc0c475f2895e.jpg',
      isVerified: true,
      chats: [],
      followers: [],
      photos: [],
      posts: []
    };
  }
}
