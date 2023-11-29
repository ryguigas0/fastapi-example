from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models import session
from models.post import Post
from models.comment import Comment


router = APIRouter(prefix="/api/posts")


@router.get("/")
def read_posts(detail_level: int = 1):
    query = session.query(Post).all()

    p_views = list(map(lambda p: p.to_view(detail_level), query))

    return JSONResponse(content=p_views)


@router.post("/")
def create_post(title: str):
    post = Post(title=title)
    session.add(post)
    session.commit()

    return JSONResponse(content=post.to_view())


@router.get("/{post_id}")
def get_post(post_id: str, detail_level: int = 1):
    post = (
        session.query(Post)
        .filter_by(post_id=post_id)
        .join(Comment, isouter=True)
        .first()
    )

    return JSONResponse(content=post.to_view())


@router.put("/{post_id}")
def put_post(post_id: str, title: str):
    post = session.query(Post).filter_by(post_id=post_id).first()

    post.title = title
    session.commit()

    return JSONResponse(content=post.to_view())


@router.delete("/{post_id}")
def delete_post(post_id: str):
    rowcount = session.query(Post).filter_by(post_id=post_id).delete()

    session.commit()

    if rowcount == 1:
        return JSONResponse(content={"msg": "Post deleted!"})
    else:
        return JSONResponse(content={"msg": "Post not found!"}, status_code=404)
