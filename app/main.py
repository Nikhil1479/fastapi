from typing import Optional
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

'''
 The below class represents a post with a title and content.
 It is extending pydantic.BaseModel for data validation.
'''


class Post(BaseModel):
    title: str
    content: str
    # If the argument is not passed it will default to True.
    published: bool = True
    rating: Optional[int] = None  # Optional field, sets to none if not
    # type: str = "Response"


app = FastAPI()

# Database Connection
# The code block you provided is attempting to establish a connection to a PostgreSQL database using
# the `psycopg2` library.
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='niks1479', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB Connection Successful")
        break
    except Exception as error:
        time.sleep(2)
        print("DB Connection failed")
        print("Error: ", error)

# Routes


@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    response = db.query(models.Post).all()
    print(type(response[0]))
    return {"data": response}


"""
    The function returns a JSON response with a message indicating that it is a social media API.
    :return: The message "social media api" is being returned.
"""


@app.get("/")
def root():
    return {"message": "social media api"}


# Route for reading posts
"""
    This function retrieves all posts from a database table and returns them as a JSON response.
    :return: a dictionary with a key "data" and the value being the result of the SQL query, which is a
    list of posts.
"""


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * from posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


# Route for creating posts
"""
    The above function creates a new post in a database table called "posts" and returns the newly
    created post.
    
    :param payload: The parameter `payload` is of type `Post`, which is likely a data model or class
    representing the structure of a post. It contains the following attributes:
    :type payload: Post
    :return: a dictionary with the key 'data' and the value being the newly created post.
"""


@app.post("/posts", status_code=status.HTTP_201_CREATED)  # Default Status Code
def createPosts(payload: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING * """,
    #                (payload.title, payload.content, payload.published, payload.rating))
    # new_post = cursor.fetchone()
    # conn.commit()

    # Unpacking a dictionary, passing the values and Post class constructor is taking those values mapping to keys.
    new_post = models.Post(**payload.model_dump())

    #! deprecated, used in previous version, now using dictionary unpacking.
    # new_post = models.Post(title=payload.title, content=payload.content,
    #    published=payload.published, rating=payload.rating)

    db.add(new_post)
    db.commit()

    # Fetch the new post that was created, and assign it to th new_post object
    db.refresh(new_post)
    return {'data': new_post}


# Route for reading the latest post
"""
    The function `get_latest_post` retrieves the latest post from a database table called "posts" and
    returns it as a JSON response.
    :return: The code is returning a JSON object with the latest post from the "posts" table in the
    database. The post is retrieved by executing a SQL query that selects all columns from the "posts"
    table and orders them by the "id" column in descending order. The "fetchone()" method is then used
    to retrieve the first row of the result set, which represents the latest post. The JSON
"""


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * from posts ORDER BY id DESC""")
    latest_post = cursor.fetchone()
    return {'data': latest_post}


# Route for reading a single post
"""
    This function retrieves a post from a database based on its ID and returns the post data if found,
    or raises a 404 error if not found.
    
    :param id: The `id` parameter is an integer that represents the unique identifier of a post. It is
    used to retrieve a specific post from the database
    :type id: int
    :param response: The `response` parameter is an instance of the `Response` class from the `fastapi`
    module. It is used to modify the response that will be sent back to the client
    :type response: Response
    :return: The code is returning a JSON response containing the fetched post data if a post with the
    specified ID is found in the database. If the post is not found, it raises an HTTPException with a
    status code of 404 (Not Found) and a detail message indicating that the post with the specified ID
    was not found.
"""


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts where id = %s""", (str(id)))
    fetched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if fetched_post:
        return {"data": fetched_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")


# Route for deleting a post
"""
    This function deletes a post from the database based on the provided ID and returns a 404 error if
    the ID is not found.
    
    :param id: The `id` parameter is an integer that represents the unique identifier of the post that
    needs to be deleted
    :type id: int
    """


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """DELETE from posts WHERE id = %s RETURNING *""", (str(id)))
    # conn.commit()
    # deleted_post = cursor.fetchone()

    delete_post = db.query(models.Post).filter(models.Post.id == id)

    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID:{id} not found in database")
    delete_post.delete(synchronize_session=False)
    db.commit()


# Route for updating posts
"""
    The function updates a post in the database with the given ID and returns the updated post.
    
    :param id: The `id` parameter is an integer that represents the unique identifier of the post that
    needs to be updated. It is used to identify the specific post in the database that needs to be
    updated
    :type id: int
    :param payload: The `payload` parameter is of type `Post`, which is likely a data model or class
    representing a post. It contains the updated information for the post, including the `title`,
    `content`, and `published` status
    :type payload: Post
    :return: a dictionary with the key 'data' and the value being the updated post.
"""


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, payload: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (payload.title, payload.content, payload.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    update_post_query = db.query(models.Post).filter(models.Post.id == id)
    post = update_post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID:{id} not found in database")

    update_post_query.update(payload.model_dump(), synchronize_session=False)
    db.commit()

    db.refresh(post)
    return {'data': post}
