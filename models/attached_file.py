from . import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

class AttachedFile(Base):
    __tablename__ = "attached_file"
    # __table_args__ = {'extend_existing': True}
    attached_file_id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("comment.comment_id", ondelete="CASCADE"))
    title = Column(String(255))
    created = Column(DateTime, default=func.now())
    file_path = Column(String(255))

    def to_view(self, level=0):
        return {
            "id": self.attached_file_id,
            "comment_id": self.comment_id,
            "title": self.title,
            "created": str(self.created),
            "file_path": self.file_path,
        }