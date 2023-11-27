from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
import datetime
import uvicorn

app = FastAPI()

user = "root"
password = "root"
mysql = "localhost:3306"
database = "prova"

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{user}:{password}@{mysql}/{database}?charset=utf8mb4"
)

engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()


class Post(Base):
    __tablename__ = "post"
    # __table_args__ = {"extend_existing": True}
    post_id = Column(Integer, primary_key=True)
    title = Column(String(255))
    created = Column(DateTime, default=func.now())
    comment = relationship("Comment")

    def to_view(self):
        return {
            "id": self.post_id,
            "title": self.title,
            "created": str(self.created),
        }


class Comment(Base):
    __tablename__ = "comment"
    __table_args__ = {"extend_existing": True}
    comment_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("post.post_id", ondelete="CASCADE"))
    post = relationship("Post")
    attached_file = relationship("AttachedFile")
    text = Column(String(255))
    created = Column(DateTime, default=func.now())
    user = Column(String(255))

    def to_view(self):
        return {
            "id": self.comment_id,
            "post_id": self.post_id,
            "text": self.text,
            "created": str(self.created),
            "user": self.user,
        }


class AttachedFile(Base):
    __tablename__ = "attached_file"
    # __table_args__ = {'extend_existing': True}
    attached_file_id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comment.comment_id", ondelete="CASCADE"))
    title = Column(String(255))
    created = Column(DateTime, default=func.now())
    file_path = Column(String(255))

    def to_view(self):
        return {
            "id": self.attached_file_id,
            "comment_id": self.comment_id,
            "title": self.title,
            "created": str(self.created),
            "file_path": self.file_path,
        }


Base.metadata.create_all(bind=engine)

# @app.get('/')
# def hello():
#     return JSONResponse(content={'msg': 'Hello world'})


@app.get("/api/posts")
def read_posts():
    query = session.query(Post).join(Comment, isouter=True).all()

    p_views = []
    for p in query:
        p_view = p.to_view()
        c_views = []
        for c in p.comment:
            c_views.append(c.to_view())
        p_view["comments"] = c_views
        p_views.append(p_view)

    return JSONResponse(content=p_views)


@app.post("/api/posts")
def create_post(title: str):
    post = Post(title=title)
    session.add(post)
    session.commit()

    return JSONResponse(content=post.to_view())


@app.get("/api/posts/{post_id}")
def get_post(post_id: str):
    post = (
        session.query(Post)
        .filter_by(post_id=post_id)
        .join(Comment, isouter=True)
        .first()
    )

    p_view = post.to_view()
    c_views = []
    for c in post.comment:
        c_views.append(c.to_view())
    p_view["comments"] = c_views

    return JSONResponse(content=p_view)


@app.put("/api/posts/{post_id}")
def put_post(post_id: str, title: str):
    post = session.query(Post).filter_by(post_id=post_id).first()

    post.title = title
    session.commit()

    return JSONResponse(content=post.to_view())


@app.delete("/api/posts/{post_id}")
def delete_post(post_id: str):
    rowcount = session.query(Post).filter_by(post_id=post_id).delete()

    session.commit()

    if rowcount == 1:
        return JSONResponse(content={"msg": "Post deleted!"})
    else:
        return JSONResponse(content={"msg": "Post not found!"}, status_code=404)


@app.get("/api/comments")
def read_comments():
    query = session.query(Comment).join(AttachedFile, isouter=True).all()

    c_views = []
    for c in query:
        c_view = c.to_view()
        a_views = []
        for a in c.attached_file:
            a_views.append(a.to_view())
        c_view["attached_files"] = a_views
        c_views.append(c_view)

    return JSONResponse(content=c_views)


@app.post("/api/comments")
def create_comment(post_id: int, text: str, user: str):
    comment = Comment(post_id=post_id, text=text, user=user)
    session.add(comment)
    session.commit()

    return JSONResponse(content=comment.to_view())


@app.get("/api/comments/{comment_id}")
def get_comment(comment_id: str):
    c = (
        session.query(Comment)
        .filter_by(comment_id=comment_id)
        .join(AttachedFile, isouter=True)
        .first()
    )

    c_view = c.to_view()
    a_views = []
    for a in c.attached_file:
        a_views.append(a.to_view())
    c_view["attached_files"] = a_views

    return JSONResponse(content=c_view)


@app.put("/api/comments/{comment_id}")
def put_comment(comment_id: str, post_id: int, text: str, user: str):
    comment = session.query(Comment).filter_by(comment_id=comment_id).first()

    comment.post_id = post_id
    comment.text = text
    comment.user = user
    session.commit()

    return JSONResponse(content=comment.to_view())


@app.delete("/api/comments/{comment_id}")
def delete_comment(comment_id: str):
    rowcount = session.query(Comment).filter_by(comment_id=comment_id).delete()

    session.commit()

    if rowcount == 1:
        return JSONResponse(content={"msg": "Commnet deleted!"})
    else:
        return JSONResponse(content={"msg": "Comment not found!"}, status_code=404)


@app.get("/api/attached_files")
def read_attached_files():
    query = session.query(AttachedFile).all()

    a_views = []
    for a in query:
        a_views.append(a.to_view())

    return JSONResponse(content=a_views)


@app.post("/api/attached_files")
def create_attached_file(comment_id: int, title: str, file_path: str):
    attached_file = AttachedFile(
        comment_id=comment_id, title=title, file_path=file_path
    )
    session.add(attached_file)
    session.commit()

    return JSONResponse(content=attached_file.to_view())


@app.get("/api/attached_files/{attached_file_id}")
def get_attached_file(attached_file_id: str):
    attached_file = (
        session.query(AttachedFile).filter_by(attached_file_id=attached_file_id).first()
    )

    return JSONResponse(content=attached_file.to_view())


@app.put("/api/attached_files/{attached_file_id}")
def put_attached_file(
    attached_file_id: int, comment_id: int, title: str, file_path: str
):
    attached_file = (
        session.query(AttachedFile).filter_by(attached_file_id=attached_file_id).first()
    )

    attached_file.comment_id = comment_id
    attached_file.title = title
    attached_file.file_path = file_path
    session.commit()

    return JSONResponse(content=attached_file.to_view())


@app.delete("/api/attached_files/{attached_file_id}")
def delete_attached_file(attached_file_id: str):
    rowcount = (
        session.query(AttachedFile)
        .filter_by(attached_file_id=attached_file_id)
        .delete()
    )

    session.commit()

    if rowcount == 1:
        return JSONResponse(content={"msg": "Commnet deleted!"})
    else:
        return JSONResponse(content={"msg": "Comment not found!"}, status_code=404)


if __name__ == "__main__":
    uvicorn.run(app, port=3000)
