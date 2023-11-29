from fastapi import APIRouter
from fastapi.responses import JSONResponse
from models import session
from models.attached_file import AttachedFile


router = APIRouter(prefix="/api/attached_files")


@router.get("/")
def read_attached_files():
    query = session.query(AttachedFile).all()

    a_views = list(map(lambda a: a.to_view(), query))

    return JSONResponse(content=a_views)


@router.post("/")
def create_attached_file(comment_id: int, title: str, file_path: str):
    attached_file = AttachedFile(
        comment_id=comment_id, title=title, file_path=file_path
    )
    session.add(attached_file)
    session.commit()

    return JSONResponse(content=attached_file.to_view())


@router.get("/{attached_file_id}")
def get_attached_file(attached_file_id: str):
    attached_file = (
        session.query(AttachedFile).filter_by(attached_file_id=attached_file_id).first()
    )

    return JSONResponse(content=attached_file.to_view())


@router.put("/{attached_file_id}")
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


@router.delete("/{attached_file_id}")
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
