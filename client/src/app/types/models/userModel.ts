export interface IUser {
	id: string;
	email: string;
	password: string; // hash
	isVerified: boolean;
	fname: string;
	lname: string;
	age: number;
	avatar: string; // source (link) image
	chats: string[]; // chat id list
	posts: string[]; // post id list
	photos: string[]; // photo id list
}
