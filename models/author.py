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
    authors = []
    for a in db.query(Author).all():
        authors.append(a.to_view())
    return JSONResponse(content=authors, status_code=200)

def get(author_id: int):
    maybe_author = db.query(Author).get(author_id)
    if maybe_author != None:
        return JSONResponse(content=maybe_author.to_view(), status_code=200)
    else:
        return JSONResponse(content={'msg': 'author not found'}, status_code=404)

def create(name: str):
    author = Author(name=name)
    try:
        db.commit()
        return JSONResponse(content=author.to_view(), status_code=201)
    except SQLAlchemyError:
        return JSONResponse(content={'error': 'invalid author name'}, status_code=400)

def update(author_id: int, name: str):
    author = db.query(Author).get(author_id)
    if author != None:
        try:
            author.name = name
            db.commit()
            return JSONResponse(content=author.to_view(), status_code=200)
        except SQLAlchemyError:
            return JSONResponse(content={'error': 'invalid author name'}, status_code=400)
    else:
        return JSONResponse(content={'msg': 'author not found'}, status_code=404)

def delete(author_id: int):
    rowcount = db.query(Author).filter(Author.id == author_id).delete(synchronize_session='fetch')
    #session.query(User).filter(User.name == "squidward").delete(synchronize_session="h")
    if rowcount > 0:
        return JSONResponse(content={'msg': 'author deleted'}, status_code=200)
    else:
        return JSONResponse(content={'msg': 'author not found'}, status_code=404)