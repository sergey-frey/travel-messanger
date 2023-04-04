from fastapi import Depends, HTTPException
from sqlalchemy import insert, select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from server.backend.db.models import Post
from server.backend.schemas.post import PostUpdate


async def _create_post(post, session: AsyncSession):
    db_post = Post(title=post.title, content=post.content, owner=post.owner)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post


async def _read_posts(session: AsyncSession, skip: int = 0, limit: int = 5, ):
    posts = await session.execute(Post.select().offset(skip).limit(limit))
    return posts.scalars().all()


async def _update_post(post_id: int, post: PostUpdate, session: AsyncSession):
    session_post = await session.get(Post, post_id)
    if not session_post:
        raise HTTPException(status_code=404, detail="Post not found")
    session_post.title = post.title
    session_post.content = post.content
    await session.commit()
    await session.refresh(session_post)
    return session_post


async def _delete_post(post_id: int, session: AsyncSession):
    session_post = await session.get(Post, post_id)
    if not session_post:
        raise HTTPException(status_code=404, detail="Post not found")
    await session.delete(session_post)
    await session.commit()
    return {"message": "Post deleted successfully"}
