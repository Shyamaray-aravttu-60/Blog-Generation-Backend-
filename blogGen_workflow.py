from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_core.output_parsers import StrOutputParser , PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel , Field

load_dotenv()
model = ChatGroq(model="openai/gpt-oss-120b")
parser = StrOutputParser()

class BlogResponse(BaseModel):
    blog: str = Field(description='this field of blog')

class OutlineResponse(BaseModel):
    outline: str = Field(description='this field of outline')


def llm_outline_gen(state:PromptChainingState):
    topic = state['topic']
    prompt = PromptTemplate(template='Generate the outline about the {topic},{format_instructions}',input_variables=['topic','format_instructions'])
    outline_parser = PydanticOutputParser(pydantic_object=OutlineResponse)
    chain = prompt | model | outline_parser
    state['outline'] = chain.invoke({'topic': topic,'format_instructions':outline_parser.get_format_instructions()}).outline
    return state

def llm_blog_gen(state:PromptChainingState):
    topic = state['topic']
    outline = state['outline']
    prompt = PromptTemplate(template='Generate the blog about the {topic} and hear is the given outline \n {outline} \n {format_instructions} ',
                            input_variables=['topic','outline','format_instructions'])
    blog_parser = PydanticOutputParser(pydantic_object=BlogResponse)
    chain = prompt | model | blog_parser
    state['blog'] = chain.invoke({'topic': topic,'outline':outline,'format_instructions':blog_parser.get_format_instructions()}).blog
    return state

#%%
# defining the state
class PromptChainingState(TypedDict):
    topic:str
    outline:str
    blog:str

# create a graph
graph = StateGraph(PromptChainingState)

# add the nodes to the graph
graph.add_node('llm_outline_gen',llm_outline_gen)
graph.add_node('llm_blog_gen',llm_blog_gen)

# add the edges to a graph
graph.add_edge(START,'llm_outline_gen')
graph.add_edge('llm_outline_gen','llm_blog_gen')
graph.add_edge('llm_blog_gen',END)

# compile the graph
workflow = graph.compile()

