from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import json
load_dotenv()

documents = SimpleDirectoryReader("data").load_data()

index = VectorStoreIndex.from_documents(documents) # vectors

openai_llm = OpenAI(model="gpt-5.5")

query_engine = index.as_query_engine( llm=openai_llm )

app = FastAPI()

class Chatrequest(BaseModel):
    user_msg: str

@app.post("/llama-chat")
def llama_chat(req : Chatrequest):
    print(req)
    prompt = f"""
    You are AI sales assistant for softwareSchool, we are providing coding classes in telugu.

    guide, qualify, suggest best suitable courses based on user profile and background.

    if they want to talk to us, we are avaibale from 10am to 6pm IST

    Do not return data inside json mardown or code block.
    always return data in JSOn format only

    {{
    "course": "user interested course",
    "score": "cold, warn, hot, ready to pay",
    "message": "ai reply",
    "asking_for_call": "true if user is asking for call else false",
    "prefered_time_slot": "users preferred call date and time in IST format DD-MM-YYYY mm:ss IST",
    "mobile_number": "user mobile number"
    }}
    conversation history: ""

    User input: { req.user_msg }
    """
    response = query_engine.query(prompt)
    response = json.loads(response.response)
    return response

