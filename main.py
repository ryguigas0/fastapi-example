from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

# .env
user = "root"
password = "root"
mysql = "localhost:3306"
database = "fastapi_example"

# ========= INIT =========

# Create REST API
app = FastAPI()

# Connect to DB
engine = create_engine(f"mysql+pymysql://{user}:{password}@{mysql}/{database}?charset=utf8mb4")

# Create DB session
Sessionlocal = sessionmaker(autoflush=False, bind=engine)
session = Sessionlocal()

# ========= MODEL =========
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256))
    email = Column(String(256))
    password = Column(String(256))

# Create models on DB
Base.metadata.create_all(bind=engine)

# ========= CONTROLLER & VIEW =========
# @ -> Access class properties
@app.get("/users")
def read_users():
    users = session.query(User).all() # controller
    view = []
    for u in users:
        view.append(user_view(u))
    return JSONResponse(content=view) # view

@app.post("/users")
def create_user(name: str, email: str, password: str):
    user = User(name=name, email=email, password=password)
    session.add(user)
    session.commit()
    return JSONResponse(content=user_view(user), status_code=201)

@app.get("/users/{user_id}")
def get_user(user_id: int, password: str):
    user = session.query(User).filter_by(id= user_id).first()
    if user == None:
        return JSONResponse(content={'message': "User not found!"}, status_code=404)
    elif password == user.password:
        user_resp = user_view(user)
        user_resp['message'] = 'Login successful!'
        return JSONResponse(content=user_resp, status_code=202)
    else:
        return JSONResponse(content={'message': "Wrong password!"}, status_code=403)

# @app.delete("/users/{id}")

# @app.put("/users/{id}")


# ========= VIEW =========
def user_view(user: User):
    return {'id': user.id, 'email': user.email, 'name': user.name}
