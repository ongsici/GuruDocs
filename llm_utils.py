from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os
import shutil


def get_pypdf_text(file_paths):
    for file_path in file_paths:
        loader = PyPDFLoader(os.path.abspath(file_path))
        pages = loader.load()

    # TODO: need to fix this, only returns 1 file
    return pages


def get_document_chunks(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 150
    )
    chunks = text_splitter.split_documents(pages)
    print(f'Completed splitting chunks')
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OllamaEmbeddings()
    persist_directory = 'docs/chroma/'
    # cleanup
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    os.makedirs(persist_directory, exist_ok=True)
    print(f'Starting storing chunks as embeddings into vector DB')
    
    vectorstore = Chroma.from_documents(
        documents=text_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f'Completed storing chunks in vector DB')
    return vectorstore


def get_conversation_chain(vectorstore, model_option):
    llm = ChatOllama(model=model_option, temperature=0)

    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
        )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain