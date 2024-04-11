from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.api_data_models import FormDataInput, SummaryInput, QueryInput, newQueryInput
import os
import uuid
from api.llm_utils import get_pypdf_text, get_document_chunks, get_vectorstore, get_conversation_chain, get_summary, conversational_rag_chain
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
    print(tmp_dir)
    os.makedirs(tmp_dir, exist_ok = True)

    persist_directory = 'docs/chroma/'
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    os.makedirs(persist_directory, exist_ok=True)

    for index, file_data in enumerate(item.files):
        pages = None
        vectorstore = None
        chunks = None
        print(len(file_data))
        base64string = base64.b64decode(file_data)

        file_path = os.path.join(tmp_dir, f'file_{index}.pdf')
        with open(file_path, 'wb') as f:
            f.write(base64string)

        pages = get_pypdf_text(file_path)
        pages_uuid = str(uuid.uuid4())
        pages_store[pages_uuid] = pages
        pages_uuid_list.append(pages_uuid)
    
        # Get document chunks
        chunks = get_document_chunks(pages)
    
        # Get vectorstore
        vectorstore = get_vectorstore(chunks, persist_directory)
    
        vectorstore_uuid = str(uuid.uuid4())
        vectorstore_dict[vectorstore_uuid] = vectorstore
        vectorstore_uuid_list.append(vectorstore_uuid)
    print(f'pages uuid list {pages_uuid_list}')
    print(f'vectorstore uuid list {vectorstore_uuid_list}')
    return {"pages_uuid_list": pages_uuid_list,
            "vectorstore_uuid_list": vectorstore_uuid_list}

@app.post("/query")
def query(item: QueryInput):

    conversation_chain = get_conversation_chain(vectorstore_dict[item.vectorstore_id], item.model_option)
    # conversation_chain_store["conversation_chain"] = conversation_chain
    response = conversation_chain({'question': item.user_query})

    return {"response": response}

@app.post("/newquery")
def newQuery(item:newQueryInput):

    conversation_rag = conversational_rag_chain(vectorstore_dict[item.vectorstore_id], item.model_option)
    response = conversation_rag.invoke(
        {"input":item.user_query},
        config={
            "configurable":{"session_id":item.session_id}
        },
    )["answer"]
    # response = conversation_rag({'question': item.user_query})

    return {"response": response}
    

@app.post("/summary")
def summary(item: SummaryInput):
    summary_list = []

    for item_page_id in item.pages_id:
        summary = get_summary(pages_store[item_page_id], item.model_option)
        summary_list.append(summary)

    return {"summary": summary_list}
