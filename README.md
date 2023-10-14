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