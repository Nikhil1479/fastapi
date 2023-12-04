from pydantic import BaseModel
from typing import Optional


'''
 The below class represents a post with a title and content.
 It is extending pydantic.BaseModel for data validation.
'''


class PostBase(BaseModel):
    title: str
    content: str
    # If the argument is not passed it will default to True.
    published: bool = True
    rating: Optional[int] = None  # Optional field, sets to none if not
    # type: str = "Response"


class PostCreate(PostBase):
    pass
