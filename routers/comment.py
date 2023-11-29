from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models import session
from models.comment import Comment
from models.attached_file import AttachedFile


router = APIRouter(prefix="/api/comments")


@router.get("/")
def read_comments(detail_level: int = 1):
    query = session.query(Comment).join(AttachedFile, isouter=True).all()

    c_views = list(map(lambda c: c.to_view(detail_level), query))

    return JSONResponse(content=c_views)


@router.post("/")
def create_comment(post_id: int, text: str, user: str):
    comment = Comment(post_id=post_id, text=text, user=user)
    session.add(comment)
    session.commit()

    return JSONResponse(content=comment.to_view())


@router.get("/{comment_id}")
def get_comment(comment_id: str, detail_level: int = 1):
    comment = (
        session.query(Comment)
        .filter_by(comment_id=comment_id)
        .join(AttachedFile, isouter=True)
        .first()
    )

    return JSONResponse(content=comment.to_view(detail_level))


@router.put("/{comment_id}")
def put_comment(comment_id: str, post_id: int, text: str, user: str):
    comment = session.query(Comment).filter_by(comment_id=comment_id).first()

    comment.post_id = post_id
    comment.text = text
    comment.user = user
    session.commit()

    return JSONResponse(content=comment.to_view())


@router.delete("/{comment_id}")
def delete_comment(comment_id: str):
    rowcount = session.query(Comment).filter_by(comment_id=comment_id).delete()

    session.commit()

    if rowcount == 1:
        return JSONResponse(content={"msg": "Commnet deleted!"})
    else:
        return JSONResponse(content={"msg": "Comment not found!"}, status_code=404)
