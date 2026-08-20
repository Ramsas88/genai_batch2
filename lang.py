from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI
from pydantic import BaseModel
load_dotenv()
app = FastAPI()

llm_client = ChatOpenAI(model="gpt-5.5")

# response = llm_client.invoke("Explain RAG")

# print( response )

inp_rag =""" 
1. AI Powered ReactJS — ₹8,000 (MRP ₹10,000) | 4-yr video access | Amazon UI Clone project With Payment Gateway Integration & Project Deployment on AWS Server | Covers: HTML, CSS, Bootstrap, JS, TypeScript, ReactJS, Redux, Tailwind, Git, AI Basics, API Integration, API security | syllabus: https://www.softwareschool.co/c/live-react-classes | Demo link: https://www.youtube.com/playlist?list=PLnO7r_Qz2pmWB_ktYB5t6nfFtdXYHzTDE 
2. AI Powered SpringBoot — ₹8,000 (MRP ₹10,000) | 4-yr video access | Amazon Backend APIs Project & Deployment On AWS Servers | Covers: Java, MySQL, SpringBoot, Microservices, AWS, Docker, K8s, Redis, JUnit, AI Basics, AI Integration, Spring Security, Sending Emails, Batch Processing | syllabus: https://www.softwareschool.co/c/live-java-backend-developer-classes | Demo Link: https://www.youtube.com/playlist?list=PLnO7r_Qz2pmWuu0Hdf-fphS7PbH_o2ogj 
3. Java Fullstack (ReactJS + SpringBoot) — ₹16,000 (MRP ₹20,000) | Covers: Java, MySQL, SpringBoot, Microservices, AWS, Docker, K8s, Redis, JUnit, Spring Security, Sending Emails, Batch Processing, HTML, CSS, Bootstrap, JS, TypeScript, ReactJS, Redux, Tailwind, Git, AI Basics, AI Integration, API Integration, API security | syllabus: https://www.softwareschool.co/c/live-java-reactja-fullstack-developer-classes | Demo links: https://www.youtube.com/playlist?list=PLnO7r_Qz2pmWB_ktYB5t6nfFtdXYHzTDE https://www.youtube.com/playlist?list=PLnO7r_Qz2pmWuu0Hdf-fphS7PbH_o2ogj 
4. Gen AI / AI Agents (LIVE COHORT) — ₹13,999 early bird (₹15,999 regular) | Existing students ₹12,999 | Starts 2nd July 2026 | Mon-Fri 7 PM IST | 8 weeks live on Zoom | https://www.softwareschool.co/gen-ai-ai-agents-course-in-telugu | Demo link: https://www.youtube.com/playlist?list=PLnO7r_Qz2pmUtsgAPuA937jZDtzTLWeJt 
5. AI Powered NodeJS, ExpressJS (LIVE COHORT) — ₹9000 early bird (₹12,999 regular) | Existing students ₹8000 | 2nd July 2026 batch cancelled | Mon-Fri 6 PM IST | 10 weeks live on Zoom | https://www.softwareschool.co/ai-powered-nodejs-expressjs-course-in-telugu | Demo link: https://www.youtube.com/watch?v=eBNSHwGTr_0&list=PLnO7r_Qz2pmU5ud0GYyprpwE07gzc7_gx&index=2 
"""

inp_history = """"""

inp_question = "do you have nodejs?"

prompt_template = """
You are AI sales agent for SoftwareSchool, we are providing coding classes in telugu.
Students will message you, please guide, qulaify and suggest best course based on user profile.

if they askign to talk to someone, we are avilable from 10am to 6pm IST on whatsapp and call. Please check their preferred timings. 

RULES:
Always return response in english only
Ask one question ata a time.
Reply with max 5 to 7 lines only and use bullet points and emojis if required.

Courses:
{rag}

Previous Conversation:
{history}

Question:
{question}

"""


# print( prompt )

# response = llm_client.invoke(prompt)

# print( response )

class ChatRequest(BaseModel):
    user_question: str

@app.post("/chat-agent")
def chat_agent(req : ChatRequest):
    prompt = PromptTemplate.from_template(prompt_template)
    prompt = prompt.format( rag= inp_rag, history= inp_history, question =  req.user_question )
    response = llm_client.invoke(prompt)
    return response.content



