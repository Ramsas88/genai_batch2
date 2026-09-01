from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
import json
import pymysql
from tools import send_email, password_reset, search_flights, hotel_booking, activate_course

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
    exp: str
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
"final_interview_result": "selected or rejected. select only if overall rating is greater than 7 and interview should be completed. if interview is not completed, keep this empty"
}}


"""
# output data:
# next_question
# current_question_overall_rating -> 
# current_question_technical_ratinh

class AiInterviewResponse(BaseModel):
    next_question: str
    current_question_overall_rating: str
    current_question_technical_ratinh: str
    current_question_communication_rating: str
    overall_interview_rating: str
    overall_technical_rating: str
    overall_coomunication_rating: str
    is_interview_completed: str
    final_interview_result: str



# don't put any jsonblock or code block.

llm_client = ChatOpenAI(model="gpt-5.5")

llm_client_with_tools = llm_client.bind_tools( [ search_flights, send_email, activate_course, hotel_booking, password_reset  ] )

llm_client = llm_client.with_structured_output(AiInterviewResponse)

def get_db_connection():
    return pymysql.connect(host="localhost", user="root", password="15081947", database="genai_b1_p3_db", cursorclass=pymysql.cursors.DictCursor )

@app.post("/interview")
def interview(req : UserData):
    history = ""

    db_con = get_db_connection()
    db_cursor = db_con.cursor()

    db_query = "select * from interview_chats where int_id=%s and user_id=%s;"
    db_cursor.execute(db_query, (req.int_id, req.user_id))
    db_data = db_cursor.fetchall()
    for row in db_data:
        history = history + f"Role: {row["message_role"]}\n Content: {row["message"]}\n"

    history = history + f"Role: user\n Content: {req.user_message}\n"

    template = PromptTemplate.from_template(prompt_template)
    prompt = template.format(exp= req.exp, tech=req.technologies, country=req.country , history=history )
    
    response = llm_client.invoke(prompt)

    response = json.loads( response.content )
    tool_response = ""

    if response["is_interview_completed"] == "yes":
        tool_prompt = f"""
        Interview is completed, send email to HR. 

        interview result:
        interview status: {response["final_interview_result"]}
        overall rating: {response["overall_interview_rating"]}
        overall technical rating: { response["overall_technical_rating"] }
        overall communication rating: { response["overall_coomunication_rating"] }

        HR email: contact@ss.co
        """
        tool_response = llm_client_with_tools.invoke(tool_prompt)

        for tool in tool_response.tool_calls:
            print(tool)
            if tool["name"] == "send_email":
                send_email.invoke(tool["args"])
            if tool["name"] == "activate_course":
                activate_course.invoke(tool["args"])

        


    # # print(prompt)

    # db_insert_query = "insert into interview_chats(int_id, user_id, message, message_role) values(%s, %s, %s, %s);"
    # db_cursor.execute(db_insert_query, (req.int_id, req.user_id, req.user_message, 'user') )

    # db_insert_query = "insert into interview_chats(int_id, user_id, message, message_role) values(%s, %s, %s, %s);"
    # db_cursor.execute(db_insert_query, (req.int_id, req.user_id, response["next_question"], 'assistant') )

    db_con.commit()
    db_con.close()


    return { "status": "success", "data": response, "tools": tool_response }













