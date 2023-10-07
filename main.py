from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "my name is nikhil"}

@app.get("/post")
def get_posts():
    return {"data": "this is your post data"}

@app.post("/createpost")
def createPosts(payload: dict=Body):
    print(payload)
    return {
        'newpost': f"title: {payload['title']}, content:{payload['content']}",
    }