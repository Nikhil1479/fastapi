from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import text
from . import models, schema
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Routes
# Route for reading posts
"""
    The function `get_posts` retrieves all posts from the database and returns them as a JSON response.
    
    :param db: The `db` parameter is of type `Session` and is used to interact with the database. It is
    injected into the `get_posts` function using the `Depends` dependency injection from the `get_db`
    function. This allows you to access the database session within the function and perform database
    :type db: Session
    :return: a dictionary with a key "data" and the value being a list of all the posts retrieved from
    the database.
    """


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return {"data": posts}


# Route for creating posts
"""
    This function creates a new post by unpacking the payload dictionary and mapping its values to the
    attributes of the Post class, then adds it to the database and returns the newly created post.
    
    :param payload: The `payload` parameter is of type `schema.PostCreate`, which is a Pydantic model
    representing the data required to create a new post. It contains attributes such as `title`,
    `content`, `published`, and `rating`
    :type payload: schema.PostCreate
    :param db: The `db` parameter is of type `Session` and is used to interact with the database. It is
    obtained using the `get_db` dependency, which is responsible for creating a new database session for
    each request
    :type db: Session
    :return: a dictionary with the key 'data' and the value being the newly created post object.
    """


# Default Status Code
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def createPosts(payload: schema.PostCreate, db: Session = Depends(get_db)):

    # Unpacking a dictionary, passing the values and Post class constructor is taking those values mapping to keys.
    new_post = models.Post(**payload.model_dump())

    #! deprecated, used in previous version, now using dictionary unpacking.
    # new_post = models.Post(title=payload.title, content=payload.content,
    #    published=payload.published, rating=payload.rating)

    db.add(new_post)
    db.commit()

    # Fetch the new post that was created, and assign it to th new_post object
    db.refresh(new_post)
    return new_post


# Route for reading the latest post
"""
    This function retrieves the latest post from the database and returns it as a response.
    
    :param db: The `db` parameter is of type `Session` and is used to interact with the database. It is
    obtained by calling the `get_db` function, which is a dependency that provides a database session
    for the route function
    :type db: Session
    :return: a JSON response with the latest post data. The response will have a key "data" which will
    contain the details of the latest post.
    """


@app.get("/posts/latest", response_model=schema.PostResponse)
def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(text('id desc')).first()
    return latest_post


# Route for reading a single post
"""
    The function `get_post` retrieves a post from the database based on its ID and returns it as a
    response, or raises a 404 error if the post is not found.
    
    :param id: The `id` parameter is an integer that represents the unique identifier of a post. It is
    used to retrieve a specific post from the database
    :type id: int
    :param db: The `db` parameter is of type `Session` and is used to interact with the database. It is
    injected into the `get_post` function using the `Depends` dependency. The `get_db` function is
    responsible for creating a new database session and returning it
    :type db: Session
    :return: a JSON response with the fetched post data if the post with the given id is found in the
    database. If the post is not found, it raises an HTTPException with a status code of 404 and a
    detail message indicating that the post with the given id was not found.
    """


@app.get("/posts/{id}", response_model=schema.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts where id = %s""", (str(id)))
    fetched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if fetched_post:
        return fetched_post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")


# Route for deleting a post
"""
    The `delete_post` function deletes a post with a specific ID from the database.
    
    :param id: The `id` parameter is the identifier of the post that needs to be deleted. It is of type
    `int`
    :type id: int
    :param db: The `db` parameter is of type `Session` and is used to interact with the database. It is
    obtained using the `Depends` function and the `get_db` dependency. The `Session` object represents a
    database session and provides methods for querying, inserting, updating, and deleting data
    :type db: Session
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


@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def update_post(id: int, payload: schema.PostCreate, db: Session = Depends(get_db)):
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
    return post
