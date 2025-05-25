from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select


from ..schemas import Post as PostData
from ..db import Post, get_session


post_router = APIRouter(prefix = "/post", tags = ["post"])

@post_router.get("/")
def read_root():
    return {"Message" : "From FastAPI"}


@post_router.post("/create", status_code = status.HTTP_201_CREATED, summary = "Create new post")
def create_post(data: PostData, session = Depends(get_session)):
    post = Post(**data.model_dump())
    session.add(post)
    return post



@post_router.get("/get_all")
def get_all_users_posts(session=Depends(get_session)):
    posts = session.scalars(select(Post)).all()
    for post in posts:
        print('!' * 15)
        print(f"Post ID: {post.id}, Title: {post.title}")
    posts = [
        PostData.model_validate(
            {
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "timestamp": post.timestamp,
                "id" : post.id
            }
        )
        for post in posts
    ]
    return posts



@post_router.get("/info/{post_id}")
def info(post_id, session = Depends(get_session)):
    post = session.scalar(select(Post).where(Post.id == post_id))
    if not post:
        raise HTTPException(
            detail = f"Post with id {post_id} not fount",
            status_code = status.HTTP_404_NOT_FOUND
        )
    else:
        return PostData.model_validate(post)
