from fastapi import FastAPI, Request, Form, HTTPException, Depends
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient #async Python driver for MongoDB based on pymongo,Async operations allow your app to handle more requests at the same time, especially when waiting on I/O (like database calls).
from passlib.context import CryptContext # used to securely hash and verify passwords in your application—especially in authentication systems like login/signup.
from pydantic import BaseModel
from bson import ObjectId
from contextlib import asynccontextmanager
from pymongo import MongoClient
from starlette.middleware.sessions import SessionMiddleware

'''When a user logs in (like in your /login/ route), 
you want to "remember" who they are between requests. You do that by storing a small piece of info in a session, which is backed by cookies.'''
import os

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = AsyncIOMotorClient(MONGO_URI)
db = client.blog_auth_db
users_collection = db.users
blog_collection = db.blogs

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

class UserReg(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@app.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup/")
async def register_user(request: Request, username: str = Form(...), password: str = Form(...)):
    existing_user = await users_collection.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(password)
    await users_collection.insert_one({"username": username, "password": hashed_password})
    return RedirectResponse("/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login/")
async def login_user( request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],):
    user = await users_collection.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    request.session["user"] = username
    '''If login is successful, stores the username in the session.
       This is how the app "remembers" who is logged in on the frontend (usually via cookies).'''
    return RedirectResponse("/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse("/", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    blogs = await blog_collection.find().to_list(length=100)
    username = request.session.get("user")
    return templates.TemplateResponse("index.html", {"request": request, "blogs": blogs, "username": username})

@app.get("/post/{post_id}", response_class=HTMLResponse)
async def read_post(request: Request, post_id: str):
    post = await blog_collection.find_one({"_id": ObjectId(post_id)})
    if not post:
        return HTMLResponse("<h1>Post Not Found</h1>", status_code=404)
    return templates.TemplateResponse("post.html", {"request": request, "post": post})

@app.get("/create_post", response_class=HTMLResponse)
async def create_post_form(request: Request):
    if "user" not in request.session:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/create_post")
async def create_post(request: Request, title: str = Form(...), content: str = Form(...)):
    if "user" not in request.session:
        raise HTTPException(status_code=403, detail="Not authenticated")
    new_post = {"title": title, "content": content}
    await blog_collection.insert_one(new_post)
    return RedirectResponse("/", status_code=303)

@app.post("/delete_post/{post_id}")
async def delete_post(post_id: str):
    result = await blog_collection.delete_one({"_id": ObjectId(post_id)})
    if result.deleted_count == 0:
        return HTMLResponse("<h1>Post Not Found</h1>", status_code=404)
    return RedirectResponse("/", status_code=303)
