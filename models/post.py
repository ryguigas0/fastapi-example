from . import Base, session
from .comment import Comment
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Post(Base):
    __tablename__ = "post"
    # __table_args__ = {"extend_existing": True}
    post_id = Column(Integer, primary_key=True)
    title = Column(String(255))
    created = Column(DateTime, default=func.now())
    comment = relationship("Comment")

    def to_view(self, level=1):
        view = {
            "id": self.post_id,
            "title": self.title,
            "created": str(self.created),
        }

        if level > 0:
            view["comments"] = list(map(lambda c: c.to_view(level - 1), self.comment))

        return view


def read_posts(level: int):
    query = session.query(Post).join(Comment, isouter=True).all()
    return list(map(lambda p: p.to_view(level), query))


def read_post(post_id: int, detail_level: int):
    post = (
        session.query(Post)
        .filter_by(post_id=post_id)
        .join(Comment, isouter=True)
        .first()
    )
    return post.to_view(detail_level)


# def create_post(title: str):
#     post = Post(title=title)
#     session.add(post)
#     session.commit()
#     return post.to_view()


# def update_post(post_id: int, title: str):
#     post = session.query(Post).filter_by(post_id=post_id).first()

#     post.title = title
#     session.commit()

#     return post.to_view()


# def delete_post(post_id: int):
#     rowcount = session.query(Post).filter_by(post_id=post_id).delete()

#     session.commit()

#     return rowcount == 1
