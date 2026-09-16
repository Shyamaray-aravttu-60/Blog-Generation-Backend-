from fastapi.params import Depends
from langchain_ollama import ChatOllama
from fastapi import FastAPI ,HTTPException , status
from sqlmodel import Session

from valSchems import ChatRequest , ChatResponse , BlogResponse , User , UserResponse , RootMessage
from blogGen_workflow import workflow
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from database import engine , get_db
from models import Users
import models


app = FastAPI(title='FastAPI with AI')
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
model = ChatGroq(model="openai/gpt-oss-120b")


@app.get('/')
def root() -> RootMessage:
    return RootMessage(message='This is demo app built by sham')


@app.post('/chat',response_model=ChatResponse)
async def chat(prompt:ChatRequest):
    response = model.invoke(prompt.prompt).content
    return ChatResponse(response=response)

@app.post('/get_blog',response_model=BlogResponse)
async def get_blog(topic:str):
    response = workflow.invoke({'topic':topic})
    return response

@app.post('/user/signup')
async def user(new_user:User , db:Session = Depends(get_db)) -> UserResponse:
    db.add(Users(**new_user.model_dump()))
    db.commit()
    return new_user


@app.get('/all_users')
async def all_users(db:Session = Depends(get_db))-> List[UserResponse]:
    return db.query(Users).all()






