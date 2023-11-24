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

@app.get("/api/authors/{author_id}")
def get_author(author_id: int):
    return author.get(author_id)

@app.put("/api/authors/{author_id}")
def update_author(author_id: int, name: str):
    return author.update(author_id, name)

@app.delete("/api/authors/{author_id}")
def delete_author(author_id: int):
    return author.delete(author_id)

Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    uvicorn.run(app, port=3000)