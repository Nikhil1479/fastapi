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
"""
    The function returns a JSON response with a message indicating that it is a social media API.
    :return: The message "social media api" is being returned.
"""
@app.get("/")
def root():
    return {"message": "social media api"}

# Route for reading posts
"""
    The function `get_posts()` returns a dictionary with a key "data" and value `my_posts`.
    :return: a dictionary with a key "data" and the value is the variable "my_posts".
"""
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Route for creating posts
"""
    The above function creates a new post by adding it to a list of posts and returns the created post
    as a dictionary.
    
    :param payload: The `payload` parameter is of type `Post`, which is likely a data model or class
    representing a post. It is used to receive the data for creating a new post
    :type payload: Post
    :return: a dictionary with the key 'data' and the value being the post_dict, which is a dictionary
    containing the post data.
"""
@app.post("/posts", status_code=status.HTTP_201_CREATED) # Default Status Code
def createPosts(payload: Post):
    post_dict = payload.model_dump() #Converting basemodel class object to python dictionary.
    post_dict['id'] = random.randint(0,1000000)
    my_posts.append(post_dict)
    return {'data': post_dict}

# Route for reading the latest post
"""
    The function `get_latest_post` returns the latest post from a list of posts.
    :return: The code is returning a JSON object with the latest post from the `my_posts` list. The JSON
    object has a key "data" which contains the value of the latest post.
"""
@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[len(my_posts)-1]
    return {'data': latest_post}

# Route for reading a single post
"""
    This function retrieves a post with a specific ID and returns it, or raises a 404 error if the post
    is not found.
    
    :param id: The `id` parameter is an integer that represents the ID of the post we want to retrieve.
    It is specified in the URL path as a path parameter
    :type id: int
    :param response: The `response` parameter is an instance of the `Response` class from the `fastapi`
    module. It is used to modify the response that will be sent back to the client
    :type response: Response
    :return: If the post is found, it will be returned. If the post is not found, an HTTPException with
    a status code of 404 (Not Found) will be raised.
    """
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f'Post with ID {id} not found'

# Route for deleting a post
"""
    This function deletes a post with a specific ID from a database.
    
    :param id: The `id` parameter is an integer that represents the unique identifier of the post to be
    deleted
    :type id: int
    :return: a Response object with a status code of 204 (NO_CONTENT).
    """
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    id_index = find_index_post(id)

    if id_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not found in database")
    my_posts.pop(id_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Route for updating posts
"""
    The function updates a post with the given ID in the database and returns the updated post.
    
    :param id: The `id` parameter is an integer that represents the unique identifier of the post that
    needs to be updated. It is used to locate the post in the database
    :type id: int
    :param payload: The `payload` parameter is of type `Post`, which is likely a model or schema class
    representing the data structure of a post. It is used to receive the updated post data from the
    client
    :type payload: Post
    :return: a dictionary with the key 'data' and the value being the updated post from the 'my_posts'
    list at the specified index.
"""
@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id: int, payload: Post):
    id_index = find_index_post(id)
    
    if id_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not found in database")

    post_dict = payload.model_dump()
    post_dict['id'] = id
    my_posts[id_index] = post_dict

    return {'data': my_posts[id_index]}