# app.py

#
# This is the full FastAPI application for your personal website.
# It now includes user authentication (login, logout, registration)
# and a comments section with a database backend.
#
# To run this application, you will need to install these new dependencies:
# `pip install passlib[bcrypt] python-multipart python-dotenv`
#
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form, Depends, HTTPException, status, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from datetime import datetime
from typing import Annotated

# --- LOAD ENVIRONMENT VARIABLES ---
# This line loads the variables from your .env file into the environment.
load_dotenv()

# --- INITIALIZE THE FASTAPI APPLICATION ---
app = FastAPI()

# A secret key is required for the SessionMiddleware
# TODO: Replace this with a long, random string in a production environment
app.add_middleware(SessionMiddleware, secret_key="a-very-secret-key-that-you-should-change")

# Mount the static files directory. This allows the app to serve
# files from the 'static' folder.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Point the templates engine to the 'templates' folder
templates = Jinja2Templates(directory="templates")

# --- DATABASE SETUP ---
#
# Retrieve the credentials from the environment variables loaded from .env
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

# Construct the database URL using the environment variables
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

# SQLAlchemy setup
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the database models
class User(Base):
    """Database model for a user."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    comments = relationship("Comment", back_populates="author")

class Comment(Base):
    """Database model for a comment."""
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(4096))
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="comments")

class ContactFormEntry(Base):
    """Database model for a contact form submission."""
    __tablename__ = "contact_form_entries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), index=True)
    message = Column(String(4096))

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- AUTHENTICATION FUNCTIONS ---
def get_user_from_db(db: Session, username: str):
    """Fetches a user from the database by username."""
    return db.query(User).filter(User.username == username).first()

def get_password_hash(password):
    """Hashes a plain-text password."""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verifies a plain-text password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user_from_session(request: Request, db: Session = Depends(get_db)):
    """A dependency to get the current logged-in user."""
    user_id = request.session.get("user_id")
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    return None

# --- ROUTES ---
# Home page route
@app.get("/")
def home(request: Request, user: User = Depends(get_current_user_from_session)):
    """Renders the main home page template."""
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

# About page route
@app.get("/about")
def about(request: Request, user: User = Depends(get_current_user_from_session)):
    """Renders the about me page template."""
    return templates.TemplateResponse("about.html", {"request": request, "user": user})

# Contact form page routes
@app.get("/contact")
def show_contact_form(request: Request, user: User = Depends(get_current_user_from_session)):
    """Renders the contact form page."""
    return templates.TemplateResponse("contact.html", {"request": request, "user": user})

@app.post("/contact")
def submit_contact_form(
    db: Annotated[Session, Depends(get_db)],
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    """Processes the submitted contact form data and saves it to the database."""
    new_entry = ContactFormEntry(name=name, email=email, message=message)
    db.add(new_entry)
    db.commit()
    # Note: Using RedirectResponse with a 303 status code is standard for form submissions
    # This has been changed to redirect to the new thank-you page
    return RedirectResponse(url="/thank-you", status_code=status.HTTP_303_SEE_OTHER)

# New route to show the thank-you page after a successful contact form submission
@app.get("/thank-you")
def show_thank_you_page(request: Request, user: User = Depends(get_current_user_from_session)):
    """Renders the thank you page."""
    return templates.TemplateResponse("thank-you.html", {"request": request, "user": user})

# User registration routes
@app.get("/register")
def show_register_form(request: Request):
    """Renders the user registration form."""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(
    db: Annotated[Session, Depends(get_db)],
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Processes new user registration."""
    if get_user_from_db(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    request.session["user_id"] = new_user.id
    return RedirectResponse(url="/comments", status_code=status.HTTP_303_SEE_OTHER)

# User login routes
@app.get("/login")
def show_login_form(request: Request):
    """Renders the user login form."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(
    db: Annotated[Session, Depends(get_db)],
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Processes user login."""
    user = get_user_from_db(db, username)
    if not user or not verify_password(password, user.hashed_password):
        # We now render the login-error.html template instead of raising an HTTPException
        return templates.TemplateResponse("login-error.html", {"request": request})
    
    request.session["user_id"] = user.id
    return RedirectResponse(url="/comments", status_code=status.HTTP_303_SEE_OTHER)

# Logout route
@app.get("/logout")
def logout_user(request: Request):
    """Logs the user out by clearing the session."""
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# Comments page routes
@app.get("/comments")
def get_comments(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user_from_session)):
    """Renders the comments page."""
    comments = db.query(Comment).order_by(Comment.created_at.desc()).all()
    return templates.TemplateResponse("comments.html", {"request": request, "user": user, "comments": comments})

@app.post("/comments")
def post_comment(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    user: User = Depends(get_current_user_from_session),
    comment_text: str = Form(...)
):
    """Processes a new comment submission."""
    # Task B: Only allow logged-in users to post comments
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You must be logged in to post a comment")

    new_comment = Comment(text=comment_text, user_id=user.id)
    db.add(new_comment)
    db.commit()
    return RedirectResponse(url="/comments", status_code=status.HTTP_303_SEE_OTHER)
