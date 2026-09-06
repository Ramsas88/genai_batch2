from fastapi import FastAPI

from mcp import ClientSession

from mcp.client.streamable_http import streamable_http_client
from pydantic import BaseModel


app = FastAPI()

class InputData(BaseModel):
    user_message: str


@app.post("/chat-with-mcp-tools")
async def chat(req: InputData):
    tools = []
    result = ""
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        print("mcp connection")
        async with ClientSession(read, write) as session:
            print('cleint session')
            await session.initialize()
            tools = await session.list_tools()

            result = await session.call_tool( "get_courses", arguments={} )







    return {  "data": result,  "tools": tools }







