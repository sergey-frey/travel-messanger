import { Content } from './contentModel';

export interface IPost extends Content {
  authorImg: string;
  authorFName: string;
  authorLName: string;
	photos: string[]; // photo id list
	text: string;
  date: moment.Moment;
}
