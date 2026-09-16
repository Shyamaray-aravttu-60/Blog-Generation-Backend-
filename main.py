from langchain_ollama import ChatOllama
from fastapi import FastAPI ,HTTPException , status
from valSchems import ChatRequest , ChatResponse , BlogResponse , User
from blogGen_workflow import workflow
from dotenv import load_dotenv
from langchain_groq import ChatGroq

app = FastAPI(title='FastAPI with AI')
load_dotenv()
model = ChatGroq(model="openai/gpt-oss-120b")

lst = []

@app.post('/chat',response_model=ChatResponse)
async def chat(prompt:ChatRequest):
    response = model.invoke(prompt.text).content
    return ChatResponse(message=response)

@app.post('/get_blog',response_model=BlogResponse)
async def get_blog(topic:str):
    response = workflow.invoke({'topic':topic})
    return response

@app.post('/user/signup')
async def user(new_user:User):
    lst.append(new_user)
    raise HTTPException(status.HTTP_201_CREATED,detail='User created successfully')


@app.get('/all_users')
async def all_users():
    return lst

