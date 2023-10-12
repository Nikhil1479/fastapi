from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import random
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

# Array to store the post data coming from frontend.
my_posts = [
    {'title':'title of post 1','content': 'content of post 1','published':True, 'rating':3,'id':1},
    {'title': 'title of post 2','content':'content of post 2','published':True, 'rating':4, 'id':2},
    {'title': 'title of post 2','content':'content of post 2','published':True, 'rating':4, 'id': 3},
    {'title': 'favourite food','content':'pizza ♥','published':True, 'rating':5, 'id':4},
]

# Helper functions
def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post
        
def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i

# Routes
@app.get("/")
def root():
    return {"message": "social media api"}

# Route for reading posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Route for creating posts
@app.post("/posts", status_code=status.HTTP_201_CREATED) # Default Status Code
def createPosts(payload: Post):
    post_dict = payload.model_dump() #Converting basemodel class object to python dictionary.
    post_dict['id'] = random.randint(0,1000000)
    my_posts.append(post_dict)
    return {'data': post_dict}

# Route for reading the latest post
@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts)-1]
    return {'data': latest_post}

# Route for reading a single post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'Post with ID {id} not found'

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    id_index = find_index_post(id)

    if id_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not found in database")
    my_posts.pop(id_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Route for updating posts
@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id: int, payload: Post):
    id_index = find_index_post(id)
    
    if id_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not found in database")

    post_dict = payload.model_dump()
    post_dict['id'] = id
    my_posts[id_index] = post_dict

    return {'data': my_posts[id_index]}