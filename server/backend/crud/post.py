from fastapi import Depends, HTTPException
from sqlalchemy import UUID, delete, insert, select, update

from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import CommunityPost, Post, UserPost


async def _create_post(post, session: AsyncSession):
    query = Post(title=post.title, content=post.content)
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return query


async def _read_posts(skip, limit, session: AsyncSession):
    query = select(Post).offset(skip).limit(limit)
    posts = await session.execute(query)
    return posts.scalars().all()


async def _update_post(post_id: UUID, post, session: AsyncSession):
    query = (
        update(Post)
        .where(Post.id == post_id)
        .values(title=post.title, content=post.content)
        .returning(Post)
    )
    post_to_update = await session.execute(query)
    update_user_id_row = post_to_update.fetchone()
    if update_user_id_row:
        await session.commit()
        return update_user_id_row[0]
    await session.refresh(post_to_update)
    return post_to_update


async def _delete_post(post_id: UUID, session: AsyncSession):
    query = delete(Post).where(Post.id == post_id)
    post_to_delete = await session.execute(query)
    if post_to_delete:
        await session.commit()
        return {"message": "Post deleted"}


async def user_create_post(owner_id: UUID, post_id: UUID, session: AsyncSession):
    query = UserPost(owner_id=owner_id, post_id=post_id)
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return query


async def community_create_post(
    community_id: UUID, post_id: UUID, session: AsyncSession
):
    query = CommunityPost(community_id=community_id, post_id=post_id)
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return query
