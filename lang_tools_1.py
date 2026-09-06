from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
load_dotenv()


llm_client = ChatOpenAI(model="gpt-5.5")

internet_search_tool = DuckDuckGoSearchRun()

results = internet_search_tool.run("openai ipo")

print(results)


prompt = f"""

summarize and give me data in bullet points

data:
{results  }
"""

ai_response = llm_client.invoke(prompt)

print(ai_response.content)

"""
pip install langchain-community langchain-experimental
API calling tool
File handling tools
DB tool
DuckDuckGo search
pythontool
"""



