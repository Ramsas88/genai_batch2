from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from fastapi import FastAPI
from pydantic import BaseModel
import json

load_dotenv()

app = FastAPI()


class ChatRequest(BaseModel):
    user_msg: str

llm_client = ChatOpenAI(model="gpt-5.5")

@app.post("/chat-with-db")
def chat_with_db( req: ChatRequest ):

    prompt = f"""

    You are a SQL expert.

    Convert user message into sql query.

    Tables:
    users: user_id, name, email, password, is_active
    orders: order_id, user_id, product_id, price, payment_status (success, failed, pending ), payment_mode (cod, cc, dc, upi, nb), order_placed_on
    products: product_id, title, price, description, in_stock (yes, no), stock_count

    always retuhnr response in JSON format only, don't put it inside code blocks or quotes.

    {{
        "sql_query": "",
        "is_sql_query_generated": "yes or no"
    }}

    User message: { req.user_msg }

    """

    ai_response = llm_client.invoke(prompt)
    ai_response = json.loads(ai_response.content)

    return { "message": ai_response }



