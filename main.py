from fastapi import FastAPI, UploadFile, File
import chromadb
import openai
import uuid
from pypdf import PdfReader
from docx import Document
from pydantic import BaseModel
import pymysql

app = FastAPI()


chroma_client = chromadb.PersistentClient("./chroma_db")
courses_collection = chroma_client.get_or_create_collection( name="courses" )

test_cllection = chroma_client.get_or_create_collection( name="test_embed")

openai_client = openai.OpenAI( api_key="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" )


@app.get("/")
def index():
    return { "message": "server running" }


@app.get("/add-data")
def add_data():
    data = [
        'AI Powered',
        'ReactJS — ₹8,000',
        '(MRP ₹10,000) |',
        '4-yr video access',
        '| Amazon UI',
        'Clone project',
        'With Payment',
        'With Payment Gateway',
        'Integration &',
        'Project',
        'Deployment on AWS Server'
    ]
    response = []
    for chunk in data:
        print( chunk )
        vectors = openai_client.embeddings.create( input= chunk, model='text-embedding-3-small' )
        print( vectors )
        id = uuid.uuid4()
        courses_collection.add( ids=[ str(id)  ] , documents=[chunk], embeddings=[ vectors.data[0].embedding ]  )
        response.append( { "id":  uuid.uuid4(), "data":chunk, "vector": vectors.data[0].embedding  } )

    return { "message": "Data added successfully", "data":  response }


def process_pdf(file):
    print("processing pdf")
    pdf_reader = PdfReader(file.file)
    data = ""
    for page in pdf_reader.pages:
        data = data + page.extract_text()

    return data

def process_document(file):
    print("processing docuemnt")
    doc_reader = Document(file.file)
    data = ""
    for para in doc_reader.paragraphs:
        data = data + para.text

    return data

def process_text(file):
    print("processing text")
    data = file.file.read()
    return str(data)

def convert_to_chunks(data):
    chunk_size = 200
    chunks = []

    for index in range(0, len(data), chunk_size ):
        # print(index)
        # chun_data = data
        # print( data[index: index + chunk_size] )
        # data[0:3]
        # data[3: 6]
        # data[ 6 : 9]
        # print( data[index: index + chunk_size] )
        chunks.append( str(data[index: index + chunk_size]) )
    return chunks

# data[start posting : end psotion]
# abcdefghijklmnopqrstuvwxyz

# abc
# def
# ghi
# jkl

@app.get("/test")
def test():
    return convert_to_chunks("abcdefghijklmnopqrstuvwxyz")


@app.post("/upload-file")
def upload_file(file: UploadFile = File(...) ):
    # small file = input file name & variable
    # UploadFile -> file meta data
    # File(...) -> mandatory
    # pdf, doc, text files allowed
    file_name = file.filename
    process_msg = ""
    data = ""
    if file_name.endswith(".pdf"):
        process_msg = "processing pdf"
        data = process_pdf(file)

    if file_name.endswith(".docx") or file_name.endswith(".doc"):
        process_msg = "processing document"
        data = process_document(file)

    if file_name.endswith(".txt"):
        process_msg = "processing text file"
        data = process_text(file)

    chunks = convert_to_chunks(data)
    response = []
    for chunk in chunks:
        chunk = str(chunk)
        # print(1)
        vectors =openai_client.embeddings.create(input=chunk, model='text-embedding-3-small')
        # print(2)
        id = uuid.uuid4()
        # print("####\n")
        # print( chunk )
        # print("\n####\n")
        test_cllection.add( ids=[ str(id) ], documents=[chunk], embeddings=[vectors.data[0].embedding] )
        # print(3)
        response.append({ 'id': str(id), 'data': chunk, 'vectors': vectors })

    return { "message": "file upload api", "file_data": file, "process_msg": process_msg, "data": data, 'embeds': response}


# chat
# user message
# related vectors and data
# user message, prompt, vector db data -> send to ai


# DTO classes

class ChatRequest(BaseModel):
    user_msg: str
    conv_id: str

@app.post('/chat')
def chat( chat_request : ChatRequest ):

    # print( chat_request.user_msg )
    # prompt
    # get business knowledge
    # send prompt + bk + user message -> ai

    vectors = openai_client.embeddings.create(model="text-embedding-3-small", input=chat_request.user_msg)
    # print(vectors)
    vectors = vectors.data[0].embedding
    # print(vectors)
    embed_results = test_cllection.query( query_embeddings=[vectors], n_results=3 )
    embed_results = embed_results["documents"][0]
    business_knowledge = ""
    for result in embed_results:
        business_knowledge = business_knowledge + " " + result

    conn = get_db_connection()
    query = "select * from conv_messages where conv_id = %s"
    cursor = conn.cursor()
    cursor.execute(query, ( chat_request.conv_id ))
    conv_messages = cursor.fetchall()

    messages = ""
    for msg in conv_messages:
        msg_data = f"User type: {msg["msg_from"]} and Msg: { msg["msg_text"] }\n"
        messages = messages + msg_data

    prompt = f""" 
        You are the AI Sales Assistant for Software School — a trusted Telugu coding education brand.

        SOCIAL PROOF: 1,25,000+ YouTube subscribers | 88,000+ Instagram followers | 23 students placed in last 5 months

        COURSES:
        { business_knowledge }


        ALL RECORDED COURSES INCLUDE: 4-year video access (all unlocked Day 1) | Dedicated personal mentor | Weekly 1-on-1 mentor calls | 24-hr doubt resolution via Zoom | Assignment reviews | Resume Preparation | Interview Preparation | Mock Interviews | Naukri & LinkedIn Profiles setup

        PAYMENT OPTIONS: Website https://www.softwareschool.co (cards, UPI, net banking, international — preferred) | UPI: 8019032313@ybl | Axis Bank A/c 924020026619522, IFSC: UTIB0003750, Manikonda Hyderabad

        Conversation history:
        {messages}
        user input:
        { chat_request.user_msg }
    """

    print( prompt )

    ai_response = openai_client.responses.create( model="gpt-5.5", input=prompt )
    ai_response = ai_response.output_text

    insert_query = "insert into conv_messages(conv_id, msg_from, msg_text) values(%s, %s, %s)"
    cursor.execute(insert_query, (chat_request.conv_id, "user", chat_request.user_msg ))

    insert_query = "insert into conv_messages(conv_id, msg_from, msg_text) values(%s, %s, %s)"
    cursor.execute(insert_query, (chat_request.conv_id, "assistant", ai_response))

    conn.commit()
    conn.close()



    return { "message": "chat api response", "ai_response": ai_response }


class ChatConvRequest(BaseModel):
    conv_id: str
    user_msg: str

# url: host, user, db, password: awsrd.aws.com

def get_db_connection():
    connection = pymysql.connect(host="localhost", user="root", password="15081947", database="gen_ai_b2_db", cursorclass=pymysql.cursors.DictCursor )
    return connection

@app.post("/chat-conv")
def chat_conv(req: ChatConvRequest):
    conn = get_db_connection()
    query = "select * from conv_messages where conv_id = %s"
    cursor = conn.cursor()
    cursor.execute(query, ( req.conv_id ))
    conv_messages = cursor.fetchall()

    messages = ""
    for msg in conv_messages:
        msg_data = f"User type: {msg["msg_from"]} and Msg: { msg["msg_text"] }\n"
        messages = messages + msg_data


    conn.close()
    return { "data": conv_messages, "messages": messages }


@app.post("/chat-history")
def chat_history(chat_request: ChatRequest):
    
    # print( chat_request.user_msg )
    # prompt
    # get business knowledge
    # send prompt + bk + user message -> ai

    vectors = openai_client.embeddings.create(model="text-embedding-3-small", input=chat_request.user_msg)
    # print(vectors)
    vectors = vectors.data[0].embedding
    # print(vectors)
    embed_results = test_cllection.query( query_embeddings=[vectors], n_results=3 )
    embed_results = embed_results["documents"][0]
    business_knowledge = ""
    for result in embed_results:
        business_knowledge = business_knowledge + " " + result

    conn = get_db_connection()
    query = "select * from conv_messages where conv_id = %s"
    cursor = conn.cursor()
    cursor.execute(query, ( chat_request.conv_id ))
    conv_messages = cursor.fetchall()

    messages = []
    for msg in conv_messages:
        msg_dict = { "role": msg["msg_from"], "content": msg["msg_text"]  }
        messages.append(msg_dict)
        # msg_data = f"User type: {msg["msg_from"]} and Msg: { msg["msg_text"] }\n"
        # messages = messages + msg_data
    messages.append({ "role": "user", "content": chat_request.user_msg })
    print(messages)
    print("####")
    prompt = f""" 
        You are the AI Sales Assistant for Software School — a trusted Telugu coding education brand.

        SOCIAL PROOF: 1,25,000+ YouTube subscribers | 88,000+ Instagram followers | 23 students placed in last 5 months

        COURSES:
        { business_knowledge }
        ALL RECORDED COURSES INCLUDE: 4-year video access (all unlocked Day 1) | Dedicated personal mentor | Weekly 1-on-1 mentor calls | 24-hr doubt resolution via Zoom | Assignment reviews | Resume Preparation | Interview Preparation | Mock Interviews | Naukri & LinkedIn Profiles setup

        PAYMENT OPTIONS: Website https://www.softwareschool.co (cards, UPI, net banking, international — preferred) | UPI: 8019032313@ybl | Axis Bank A/c 924020026619522, IFSC: UTIB0003750, Manikonda Hyderabad
    """

    print( prompt )

    ai_response = openai_client.chat.completions.create(model="gpt-5.5", messages=messages)
    ai_response = ai_response.choices[0].message.content

    # insert_query = "insert into conv_messages(conv_id, msg_from, msg_text) values(%s, %s, %s)"
    # cursor.execute(insert_query, (chat_request.conv_id, "user", chat_request.user_msg ))

    # insert_query = "insert into conv_messages(conv_id, msg_from, msg_text) values(%s, %s, %s)"
    # cursor.execute(insert_query, (chat_request.conv_id, "assistant", ai_response))

    # conn.commit()
    conn.close()



    return { "message": "chat api response", "ai_response": ai_response }










