import uvicorn
from models import author
from fastapi import FastAPI
from models.db import Base, engine

app = FastAPI()

@app.post("/api/authors")
def create_author(name: str):
    return author.create(name)

@app.get("/api/authors")
def list_authors():
    return author.list()

# @app.post("/api/authors")
# def create_author(name: str):
#     return author.create(name)

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app, port=3000)