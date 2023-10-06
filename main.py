from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "my name is nikhil"}

@app.get("/post")
def get_posts():
    return {"data": "this is your post data"}