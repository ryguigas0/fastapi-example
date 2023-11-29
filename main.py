from fastapi import FastAPI
from models import create_models
from routers.post import router as post_router
from routers.comment import router as comment_router
from routers.attached_files import router as attached_files_router
import uvicorn

app = FastAPI()

create_models()

app.include_router(post_router)
app.include_router(comment_router)
app.include_router(attached_files_router)


if __name__ == "__main__":
    uvicorn.run(app, port=3000)
