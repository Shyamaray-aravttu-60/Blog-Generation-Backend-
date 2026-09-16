from pydantic import BaseModel , Field , EmailStr
from typing import TypedDict

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    message: str

class BlogResponse(TypedDict):
    topic:str
    outline:str
    blog:str

class User(BaseModel):
    name : str = Field(max_length=50)
    age : int = Field(gt=0)
    email : EmailStr
    gender : str
    password: str
