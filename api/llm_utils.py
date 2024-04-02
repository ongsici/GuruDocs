from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

import os
import shutil
import pandas as pd


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

def get_embedding():
    model_name = "BAAI/bge-small-en"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": True}
    hf_embd = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
    return hf_embd

def get_vectorstore(text_chunks):
    embeddings = get_embedding()
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

def get_summary(pages, model_option):
    final_mp_data = []
    llm = ChatOllama(model=model_option, temperature=0)

    map_prompt_template = """
                      Write a summary of this chunk of text that includes the main points and any important details.
                      {text}
                      """

    map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

    combine_prompt_template = """
                        Write a concise summary of the following text delimited by triple backquotes.
                        Return your response in bullet points which covers the key points of the text.
                        ```{text}```
                        BULLET POINT SUMMARY:
                        """

    combine_prompt = PromptTemplate(
        template=combine_prompt_template, input_variables=["text"]
        )
    
    map_reduce_chain = load_summarize_chain(
                        llm,
                        chain_type="map_reduce",
                        map_prompt=map_prompt,
                        combine_prompt=combine_prompt,
                        return_intermediate_steps=True,
                    )
    map_reduce_outputs = map_reduce_chain({"input_documents": pages})
    
    for doc, out in zip(
        map_reduce_outputs["input_documents"], map_reduce_outputs["intermediate_steps"]
    ):
        output = {}
        output["file_name"] = (doc.metadata["source"])
        output["file_type"] = (doc.metadata["source"])
        output["page_number"] = doc.metadata["page"]
        output["chunks"] = doc.page_content
        output["concise_summary"] = out
        final_mp_data.append(output)

    pdf_mp_summary = pd.DataFrame.from_dict(final_mp_data)
    pdf_mp_summary = pdf_mp_summary.sort_values(
        by=["file_name", "page_number"]
    )  # sorting the dataframe by filename and page_number
    pdf_mp_summary.reset_index(inplace=True, drop=True)
    summary = pdf_mp_summary["concise_summary"].iloc[0]
    return summary