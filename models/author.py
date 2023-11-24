from fastapi.responses import JSONResponse
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from .db import Base, Database as db

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String(90))
    def to_view(self):
        return {
            'id': self.id,
            'name': self.name
        }

def list():
    authors = list(map(lambda a: a.to_view(), db.query(Author).all()))
    return JSONResponse(content=authors, status_code=200)

def get(author_id: int):
    maybe_author = db.query(Author).get(author_id)
    if maybe_author != None:
        return JSONResponse(content=maybe_author.to_view(), status_code=200)
    else:
        return JSONResponse(content=maybe_author.to_view(), status_code=404)

def create(name: str):
    author = Author(name=name)
    db.add(author)
    db.commit()
    return JSONResponse(content=author.to_view(), status_code=201)
    # try:
    #     db.commit()
    #     return JSONResponse(content=author.to_view(), status_code=201)
    # except SQLAlchemyError:
    #     return JSONResponse(content={'error': 'invalid author name'}, status_code=400)