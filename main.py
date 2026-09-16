from langchain_ollama import ChatOllama
from fastapi import FastAPI ,HTTPException , status
from valSchems import ChatRequest , ChatResponse , BlogResponse , User , UserResponse , RootMessage
from blogGen_workflow import workflow
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing import List


app = FastAPI(title='FastAPI with AI')
load_dotenv()
model = ChatGroq(model="openai/gpt-oss-120b")

lst = []

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
async def user(new_user:User) -> UserResponse:
    lst.append(new_user)
    return new_user


@app.get('/all_users')
async def all_users()-> List[UserResponse]:
    return lst

