from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

'''
 The below class represents a post with a title and content.
 It is extending pydantic.BaseModel for data validation.
'''
class Post(BaseModel): 
    title: str
    content: str
    published: bool = True # If the argument is not passed it will default to True.
    rating: Optional[int] = None # Optional field, sets to none if not
    type: str = "Response"

app = FastAPI()

@app.get("/")
def root():
    return {"message": "my name is nikhil"}

@app.get("/post")
def get_posts():
    return {"data": "this is your post data"}

@app.post("/createpost")
def createPosts(payload: Post):
    
    print(payload)
    print(payload.title)
    print(type(payload))
    # dict =  payload.model_dump() #Converting basemodel class object to python dictionary.
    # dict.update({'type': 'response'})
    return {'data': payload}