from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import RequestsPostTool
from langchain_community.utilities.requests import TextRequestsWrapper
import json
load_dotenv()

llm_client = ChatOpenAI(model="gpt-5.5")


api_wrapper =TextRequestsWrapper( headers={ "content-type": "application/json", "Authorization": "bearer sghslkgasasgsagasgasgsagasgagagagagagag" } )

api_tool = RequestsPostTool( requests_wrapper=api_wrapper, allow_dangerous_requests=True )

api_data = json.dumps({
    'url': 'https://dummyjson.com/products/add',
    'data': {
        "title": "reactjs tutorial"
    }
})

result = api_tool.run(api_data)

print( result )

