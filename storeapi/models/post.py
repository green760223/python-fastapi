from pydantic import BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int


class UserPostWithComments(BaseModel):
    comments: list[Comment]
    post: UserPost