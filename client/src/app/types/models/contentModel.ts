import { IComment } from './commentModel';
import { Reaction } from './reactionModel';

export interface Content {
	id: string;
	likes: number;
	dislikes: number;
	comments: IComment[];
	reactions: Reaction[];
}
