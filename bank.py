from fastapi import FastAPI , HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from jose  import jwt , JWTError
from datetime import datetime , timedelta
from typing import Optional


app = FastAPI(title="online bank")


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


SECRET_KEY = "" #paste ur own jwt key 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")


users ={
    # fake-database
}

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str


class Transfer(BaseModel):
    to_username : str
    amount : float


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain , hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp" : expire})
    return  jwt.encode(to_encode , SECRET_KEY,algorithm = ALGORITHM)


def get_current_user(token):
    try :
        payload = jwt.decode(token , SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in users:
            raise HTTPException(status_code=401, detail="401 Unauthorized")
        return username
    except JWTError:
        raise HTTPException(status_code=401 , detail="token invalid")


@app.post("/register")
def  register(user : UserCreate):
    if user.username in users:
        raise HTTPException(status_code=400 , detail="username exists")
    users[user.username] = {"hashed_password" : hash_password(user.password) , "balance" : 1000.0}
    return {"message" : f"Our User {user.username} has been created"}


@app.post("/login" , response_model=Token)
def login(user : UserCreate):
    db_user = users.get(user.username)
    if not db_user or not verify_password(user.password , db_user["hashed_password"]):
        raise HTTPException(status_code=401 , detail="invalid data user")
    token = create_access_token({"sub": user.username})
    return {"access_token" : token, "token_type" : "bearer"}


@app.get("/me")
def me(token : str):
    username = get_current_user(token)
    return {"username" : username , "balance" : users[username]["balance"]}


@app.post("/transfer")
def transfer(transfer: Transfer, token: str):
    sender = get_current_user(token)
    if transfer.to_username not in users:
        raise HTTPException(status_code=404 , detail="receiver not found")
    if users[sender]["balance"] < transfer.amount:
        raise HTTPException(status_code=400 , detail="insufficient balance")
    users[sender]["balance"] -= transfer.amount
    users[transfer.to_username]["balance"] += transfer.amount
    return {"message" : f"Transferred {transfer.amount} from {sender} to {transfer.to_username} successfully"}

