export interface IComment {
	from: string; // user id
	text: string;
	parentComment: Comment | null; // если это ответ на другой комментарий
	replies: Comment[];
	likes: number;
}
