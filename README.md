# FastAPI-Dev Branch
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


