import { Content } from './contentModel';

export interface IPost extends Content {
	photos: string[]; // photo id list
	text: string;
}
