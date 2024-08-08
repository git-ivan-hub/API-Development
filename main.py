from fastapi import FastAPI  
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": "This is the list of posts"}

@app.post("/createpost")
async def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} constent: {payload['content']}"}
