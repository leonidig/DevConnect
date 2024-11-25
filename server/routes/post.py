from fastapi import APIRouter, Depends, status


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
