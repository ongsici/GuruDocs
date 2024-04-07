from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.api_data_models import FilePath, SummaryInput, QueryInput, newQueryInput

import uuid

# Your existing code for functions
from api.llm_utils import get_pypdf_text, get_document_chunks, get_vectorstore, get_conversation_chain, get_summary, conversational_rag_chain

app = FastAPI()
vectorstore_dict = {}
conversation_chain_store = {}
pages_store = {}

@app.get("/ping")
def ping():
    return JSONResponse(content="OK", status_code = 200)

@app.post("/embed")
# async def embed(file_path: str):
def embed(item: FilePath):
    # Get text from PDF
    pages = get_pypdf_text([item.file_path])
    pages_uuid = str(uuid.uuid4())
    pages_store[pages_uuid] = pages
    
    # Get document chunks
    chunks = get_document_chunks(pages)
    
    # Get vectorstore
    vectorstore = get_vectorstore(chunks)
    
    vectorstore_uuid = str(uuid.uuid4())
    vectorstore_dict[vectorstore_uuid] = vectorstore

    return {"pages_id": pages_uuid,
            "vectorstore_id": vectorstore_uuid}

@app.post("/query")
# async 
def query(item: QueryInput):

    conversation_chain = get_conversation_chain(vectorstore_dict[item.vectorstore_id], item.model_option)
    # conversation_chain_store["conversation_chain"] = conversation_chain
    response = conversation_chain({'question': item.user_query})

    return {"response": response}

@app.post("/newquery")
#async
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
# async 
def summary(item: SummaryInput):
    
    # Get summary
    # print(f'type pages {type(item.pages)}')
    # for item_dict in item.pages:
    #     print(f'item dict type {type(item_dict)}')
    #     print(item_dict)
    summary = get_summary(pages_store[item.pages_id], item.model_option)

    return {"summary": summary}
