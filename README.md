# FastAPI

**FastAPI** is a modern Python web framework, very efficient in building APIs.
## Setting up Development Environment.
### Virtual Environment in Python
A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them. This is one of the most important tools that most Python developers use.
### Creating a venv
```sh
$ py -3 -m venv <venv_name>
```
This will create a virtual environment for python where we will keep al our dependencies for this project.

Once a `venv` is created we will see a folder (in our case `venv`) this folder has all the libraries we will install.
### Configuring the python interpreter in vscode. 
To configure venv python interpreter.
- Open Command Palette <kbd>CTRL</kbd> + <kbd>SHIFT</kbd> + <kbd>B</kbd>
- Search for `Python: Select Interpreter`
- Select `Enter Interpreter Path`
- Enter path to your venv `python.exe` file i.e `.\venv\Scripts\python.exe`
### Configuring terminal to connect to `venv`
#### For Command Prompt (CMD)
run `venv\Scripts\activate.bat`.
#### For Powershell
run `venv\Scripts\activate.ps1`
> Since we are done with our environment setup, let's install `fastapi`

---
## Creating a fastapi app
### Installing `fastapi`
Installing `fastapi` using `pip`
```sh
pip install fastapi[all]
```
### Creating fastapi app
To create a fastapi app we need to create an object of `FastAPI` class.
A basic fastapi app that is implementing a `get-request`.
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/") # root 
def root():
    return {"message": "my name is nikhil"}
    
@app.get("/post") # 127.0.0.1/post
def get_posts():
    return {"data": "this is your post data"}
```

To host a server `fastapi` uses `uvicorn` for deployment.
```sh
➜ uvicorn main:app --reload
```

```sh
INFO:     Will watch for changes in these directories: ['E:\\HighRadius Paid\\Python              Development\\fastapi']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [11288] using WatchFiles
INFO:     Started server process [21916]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
>This will start a server at localhost: `http://127.0.0.1:8000`.

---
## Data Validation using Pydantic
**Pydantic** is a Python library for data parsing and validation. It uses the type hinting mechanism of the newer versions of Python (version 3.6 onwards) and validates the types during the runtime. Pydantic defines **`BaseModel`** class. It acts as the base class for creating user defined models.

Payload (Sent from frontend)
```json
{
    "title": "My vacation to miami",
    "content": "checkout some awesome photos",
    "rating": 5
}
```
We need to make sure that the data we receive from frontend should be in a proper format.
So, we need to validate for this we will be using `pydantic`
### Setting up pydantic
#### Importing necessary libraries
```python
from typing import Optional
from pydantic import BaseModel
```
#### Validating Data
```python
class Post(BaseModel): 
    title: str
    content: str
    published: bool = True # If the argument is not passed it will default to True.
    rating: Optional[int] = None # Optional field, sets to none if not
    type: str = "Response"
```
`Pydantic` will automatically validate the data when passed.

We will pass data as an object of `Post` class (in our case)
```python
@app.post("/createpost")
def createPosts(payload: Post):
    print(payload)
    print(payload.title)
    print(type(payload))
    # dict =  payload.model_dump() #Converting basemodel class object to python dictionary.
    # dict.update({'type': 'response'})
    return {'data': payload}
```
> This will validate our data according to the specified datatype and structure. If the data passed is not in proper format, it will raise an exception as a response.

---
### HTTP Status Codes
[HTTP Status Code]([HTTP response status codes - HTTP | MDN (mozilla.org)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status))
HTTP response status codes indicate whether a specific [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) request has been successfully completed. Responses are grouped in five classes:
1. [Informational responses](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses) (`100` – `199`)
2. [Successful responses](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#successful_responses) (`200` – `299`)
3. [Redirection messages](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages) (`300` – `399`)
4. [Client error responses](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses) (`400` – `499`)
5. [Server error responses](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses) (`500` – `599`)
Everytime we trigger our `fastapi` in response we get a `HTTP status code` which represents the status of response, whether a `HTTP` request have been successfully completed or not.
By default fastspi sends the HTTP status response code automatically. But we have to send our custom response code for our CRUD application.
#### Using `HTTPException`
```python
from fastapi import Response, status, HTTPException

# Route for reading a single post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if post:
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID {id} not found')
```
#### Setting default status code
You can set a default `status` code for a specific route by passing the status code inside the `decorator` or `route` itself.
```python
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    id_index = find_index_post(id)
    if id_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not         found in database")
    my_posts.pop(id_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```
>This function deletes a post with a specific ID from a database.
    :param id: The id parameter is an integer that represents the unique identifier of the post to be
    deleted
    :type id: int
    :return: a Response object with a status code of 204 (NO_CONTENT).
---
## Creating a CRUD Application
CRUD stands for create, read, update and delete. Our application will be able to perform all these operations
### Reading a Post
##### Storing all our post in `my_post` list.
```python
my_posts = [
    {'title':'title of post 1','content': 'content of post 1','published':True, 
    'rating':3,'id':1},
    {'title': 'title of post 2','content':'content of post 2','published':True,  
    'rating':4, 'id':2},
    {'title': 'title of post 2','content':'content of post 2','published':True,   
    'rating':4, 'id': 3},
    {'title': 'favourite food','content':'pizza ♥','published':True, 'rating':5,            'id':4},
]
```

```python
# Route for reading posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}
```
>The function `get_posts()` returns a dictionary with a key "data" and value `my_posts`.
   :return: a dictionary with a key "data" and the value is the variable "my_posts".
>**127.0.0.1:8000/posts**
### Creating a post
```python
@app.post("/posts", status_code=status.HTTP_201_CREATED) # Default Status Code
def createPosts(payload: Post):
    post_dict = payload.model_dump() #Converting basemodel class object to python dictionary.
    post_dict['id'] = random.randint(0,1000000)
    my_posts.append(post_dict)
    return {'data': post_dict}
```
>The above function creates a new post by adding it to a list of posts and returns the created post as a dictionary.
    :param payload: The `payload` parameter is of type `Post`, which is likely a data model or class representing a post. It is used to receive the data for creating a new post
    :type payload: Post
    :return: a dictionary with the key 'data' and the value being the post_dict, which is a dictionary
    containing the post data.
    **127.0.0.1:8000/posts**
#### Sample `JSON` format for post
```json
{
    "title": "My vacation to miami",
    "content": "checkout some awesome photos",
    "rating": 5
}
```
### Updating a Post
```python
@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id: int, payload: Post):
    id_index = find_index_post(id)
    if id_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not found in database")
    post_dict = payload.model_dump()
    post_dict['id'] = id
    my_posts[id_index] = post_dict
    return {'data': my_posts[id_index]}
```
>The function updates a post with the given ID in the database and returns the updated post.
    :param id: The `id` parameter is an integer that represents the unique identifier of the post that
    needs to be updated. It is used to locate the post in the database
    :type id: int
    :param payload: The `payload` parameter is of type `Post`, which is likely a model or schema class
    representing the data structure of a post. It is used to receive the updated post data from the
    client
    :type payload: Post
    :return: a dictionary with the key 'data' and the value being the updated post from the 'my_posts'
    list at the specified index.
    >**127.0.0.1:8000/posts/2**
### Deleting a Post
```python
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    id_index = find_index_post(id)
    if id_index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not found in database")
    my_posts.pop(id_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```
>This function deletes a post with a specific ID from a database.
    :param id: The `id` parameter is an integer that represents the unique identifier of the post to be
    deleted
    :type id: int
    :return: a Response object with a status code of 204 (NO_CONTENT).
    **127.0.0.1:8000/posts/2**

---
## Introducing Databases
As of now we are storing all our post in a list of dictionaries i.e.
```python
my_posts = [
    {'title':'title of post 1','content': 'content of post 1','published':True, 
    'rating':3,'id':1},
    {'title': 'title of post 2','content':'content of post 2','published':True,  
    'rating':4, 'id':2},
    {'title': 'title of post 2','content':'content of post 2','published':True,   
    'rating':4, 'id': 3},
    {'title': 'favourite food','content':'pizza ♥','published':True, 'rating':5,            'id':4},
]
```
>But we cannot store the post like this we would be needing a robust tool to store all our post.
  For that we will be using `postgreSQL`.
### PostgreSQL 
PostgreSQL is an free open-source database system that supports both relational (SQL) and non-relational (JSON) queries.
PostgreSQL is a back-end database for dynamic websites and web applications.

### Schema for our Application

| **Name**       | **Datatype**            | **Not Null?** | **Primary Key?** | **Default**                           |
|------------|---------------------|-----------|--------------|-----------------------------------|
| id         | integer             | YES       | YES          | `nextval('posts_id_seq'::regclass)` |
| title      | character varying   | YES       | NO           |                                   |
| content    | character varying   | YES       | NO           |                                   |
| published  | boolean             | YES       |              | true                              |
| created_at | time with time zone | YES       |              | `NOW()`                             |
| rating     | integer             | NO        |              |                                   |
To interact with `postgreSQL` using python we will be needing a postgreSQL driver i.e. `psycopg2`.
### Installing `psycopg2`
```sh
pip install psycopg2
```
### Creating connection with `postgreSQL`
```python
import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='niks1479',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB Connection Successful")
        break
    except Exception as error:
        time.sleep(2)
        print("DB Connection failed")
        print("Error: ",error)
```
*`RealDictCursor` is a specialized `DictCursor` that enables to access columns only from keys (aka columns name), whereas `DictCursor` enables to access data both from keys or index number*
#### To execute a `SQl` query
```python
cursor.execute("QUERY")
example:
cursor.execute("SELECT * FROM posts*")
```
>This will return all the entries in post table.
## CRUD Application using postgreSQL
#### Connect to your db instance using the above steps:
   [[#Creating connection with `postgreSQL`]]
#### Reading Post
```python
@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * from posts")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}
```
#### Creating Posts
```python
@app.post("/posts", status_code=status.HTTP_201_CREATED) # Default Status Code
def createPosts(payload: Post):
    cursor.execute("""INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING * """, (payload.title, payload.content, payload.published, payload.rating))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}
```
#### Reading Latest Post
```python
@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC""")
    latest_post = cursor.fetchone()
    return {'data': latest_post}
```
#### Reading a single Post
```python
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * from posts where id = %s""",(str(id)))
    fetched_post = cursor.fetchone()
    if fetched_post:
        return {"data":fetched_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
```
#### Deleting a Post
```python
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    conn.commit()
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not found in database")
```
#### Updating Post
```python
@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id: int, payload: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(payload.title,payload.content,payload.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID:{id} not found in database")
    return {'data': updated_post}
```