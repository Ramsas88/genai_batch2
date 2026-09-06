from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools import RequestsGetTool
from langchain_community.utilities.requests import TextRequestsWrapper

# Request URL https://api.softwareschool.co/courses/getCoursesList
# Request Method POST
# data sample 

load_dotenv()
llm_client = ChatOpenAI(model="gpt-5.5")

api_wrapper = TextRequestsWrapper()

api_tool = RequestsGetTool( requests_wrapper=api_wrapper, allow_dangerous_requests=True )

api_result = api_tool.run("https://dummyjson.com/products")

# print( api_result )

prompt = f"""
You are Sales assistant for ecommerce website. 

user input: what is the return policy and minimum order qunatity for dog food?

data:
{api_result}
"""

ai_response = llm_client.invoke(prompt)

print( ai_response.content  )

