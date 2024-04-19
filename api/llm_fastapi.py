from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.api_data_models import FormDataInput, SummaryInput, QueryInput, newQueryInput
import os
import uuid
from api.llm_utils import get_pypdf_text, get_document_chunks, get_vectorstore, get_conversation_chain, get_summary, conversational_rag_chain, eval
from fastapi.middleware.cors import CORSMiddleware
import base64
import shutil

origins = [
    'http://localhost:3001'
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
vectorstore_dict = {}
conversation_chain_store = {}
pages_store = {}

@app.get("/ping")
def ping():
    return JSONResponse(content="OK", status_code = 200)

@app.post("/embed")
def embed(item: FormDataInput):
    pages_uuid_list = []
    vectorstore_uuid_list = []
    # Get text from PDF
    tmp_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tmp'))
    os.makedirs(tmp_dir, exist_ok = True)

    persist_directory = 'docs/chroma/'
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    os.makedirs(persist_directory, exist_ok=True)

    for index, file_data in enumerate(item.files):
        pages = None
        vectorstore = None
        chunks = None
        base64string = base64.b64decode(file_data)

        file_path = os.path.join(tmp_dir, f'file_{index}.pdf')
        with open(file_path, 'wb') as f:
            f.write(base64string)

        pages = get_pypdf_text(file_path)
        pages_uuid = str(uuid.uuid4())
        pages_store[pages_uuid] = pages
        pages_uuid_list.append(pages_uuid)
    
        # Get document chunks
        chunks = get_document_chunks(file_path)
    
        # Get vectorstore
        vectorstore = get_vectorstore(chunks, persist_directory)
    
        vectorstore_uuid = str(uuid.uuid4())
        vectorstore_dict[vectorstore_uuid] = vectorstore
        vectorstore_uuid_list.append(vectorstore_uuid)

    # clean up of tmp directory as PDF documents are not needed anymore
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    print(f'vector {vectorstore_uuid_list}')
    return {"pages_uuid_list": pages_uuid_list,
            "vectorstore_uuid_list": vectorstore_uuid_list}

@app.post("/query")
def query(item: QueryInput):

    conversation_chain, context = get_conversation_chain(vectorstore_dict[item.vectorstore_id], item.model_option, item.user_query)
    response = conversation_chain({'question': item.user_query})
    answer = response['answer']
    faithfulness, Ans_Relevancy = eval(item.user_query,answer,context,item.model_option)
    return {"response": response, "context": context, "Faithfulness": faithfulness, "Answer Relevancy Score": Ans_Relevancy}
    

@app.post("/newquery")
def newQuery(item:newQueryInput):

    conversation_rag, context = conversational_rag_chain(vectorstore_dict[item.vectorstore_id], item.model_option,item.user_query)
    generated_sesion_id = str(uuid.uuid4())
    response = conversation_rag.invoke({"input":item.user_query},config={"configurable":{"session_id":generated_sesion_id}},)["answer"]
    faithfulness, Ans_Relevancy = eval(item.user_query,response,context,item.model_option)
    return {"response": response,  "context": context, "Faithfulness": faithfulness, "Answer Relevancy Score": Ans_Relevancy}
    

@app.post("/summary")
def summary(item: SummaryInput):
    summary_list = []

    for item_page_id in item.pages_id:
        summary = get_summary(pages_store[item_page_id], item.model_option)
        summary_list.append(summary)

    return {"summary": summary_list}
