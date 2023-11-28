from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import UserSchema, DataUser
from config.db import engine
from models.users import users
from werkzeug.security import generate_password_hash, check_password_hash

user = APIRouter()

@user.get("/")
def root():
    return {"message": "Hi, I am FastAPI with a Router"}

@user.get("/api/user")
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        columns = users.columns.keys()
        user_list = [dict(zip(columns, row)) for row in result]
        
        return user_list

@user.get("/api/user/{user_id}")
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        columns = users.columns.keys()
        
        if result:
            result = dict(zip(columns, result))
            return result
        return {'response': 'None'}

@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)
        
        conn.execute(users.insert().values(new_user))
        conn.commit()
    
        return Response(status_code=HTTP_201_CREATED)
    
@user.post("/api/user/login", status_code=200)
def user_login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        if result != None:
            check_passw = check_password_hash(result[3], data_user.user_passw)
            if check_passw:
                return {
                    "status": 200,
                    "mesage": 'Access success'
                }
        return {
            "status": HTTP_401_UNAUTHORIZED,
            "mesage": 'Access Denied'
        }
    
@user.put("/api/user/{user_id}")
def update_user(data_update: UserSchema, user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        
        if result:
            encryp_passw = generate_password_hash(data_update.user_passw, "pbkdf2:sha256:30", 30)
            conn.execute(users.update().values(name=data_update.name, username=data_update.username, 
                                            user_passw=encryp_passw).where(users.c.id == user_id))
            conn.commit()
            
            result = conn.execute(users.select().where(users.c.id == user_id)).first()
            columns = users.columns.keys()
            result = dict(zip(columns, result))
            return result
        return {'response': 'None'}
    
@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))
        conn.commit()
        
        return Response(status_code=HTTP_204_NO_CONTENT)