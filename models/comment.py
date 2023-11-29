from . import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

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

    def to_view(self, level=1):
        view = {
            "id": self.comment_id,
            "post_id": self.post_id,
            "text": self.text,
            "created": str(self.created),
            "user": self.user,
        }

        if level > 0:
            view["attached_files"] = list(
                map(lambda a: a.to_view(level - 1), self.attached_file)
            )

        return view