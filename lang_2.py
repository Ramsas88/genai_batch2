from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
load_dotenv()
app = FastAPI()

"""
AI -> interview candidate based on user profile, send email

Input:
technology, exp, country, user_id, interview_id, user answer

Receive input, get history, send input data, prompt and history to AI

Save user answer and AI reply

Tool calling for email

Database:
users -> user _id, name, email, mobile

interviews -> interview_id, user_id, status, result, started on, completed on

interview_chats-> chat_id, interview_id, user_id, messafe, message_role, date time

"""

class UserData(BaseModel):
    technologies: str
    exp: int
    country: str
    user_id: int
    int_id: int
    user_message: str

prompt_template = """
You are AI interview agent for infosys technologies. Based on your profile conduct technical interviews.

Rules:
1. Ask 1 question at a time
2. Questions and their difficulty level should be based on user experience and country
3. Evaluate technical and communication skills.
4. If user is rude and unprofessional, end the interview politely
5. If user is angry or using bad words or abusing, always reply professionally.
6. User should not be able to end interview, only you can end the interview.
7. Always communicate in english only.
8. Don't ask anything personal

User Profile:
Experience:{exp}
Technologies:{tech}
Country:{country}

Previous Conversation:
{history}

Output:
Always return response in JSON format only. 
{{
"next_question": "",
"current_question_overall_rating": "0 to 10",
"current_question_technical_ratinh": "0 to 10",
"current_question_communication_rating": "0 to 10",
"overall_interview_rating": "0 to 10",
"overall_technical_rating": "0 to 10",
"overall_coomunication_rating": "0 to 10",
"is_interview_completed": "yes or no",
"final_interview_reult": "selected or rejected. select only if overall rating is greater than 7"
}}

"""
# don't put any jsonblock or code block.

llm_client = ChatOpenAI(model="gpt-5.5")

@app.post("/interview")
def interview(req : UserData):
    history = ""

    template = PromptTemplate.from_template(prompt_template)
    prompt = template.format(exp= req.exp, tech=req.technologies, country=req.country , history=history )
    
    response = llm_client.invoke(prompt)




    return { "status": "success", "data": response }













