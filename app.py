import streamlit as st
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter,RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
# from langchain.llms import HuggingFaceHub
import os
import shutil

# def get_pdf_text(pdf_docs):
#     text = ""
#     for pdf in pdf_docs:
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text

def get_pypdf_text(file_paths):
    for file_path in file_paths:
        print(f'file path {file_path}')
        print(os.path.abspath(file_path))
        loader = PyPDFLoader(os.path.abspath(file_path))
        pages = loader.load()
    print(f'PAGES TYPE {type(pages)}')
    # TODO: need to fix this, only returns 1 file
    return pages

def save_file_to_tmp(pdf_docs):
    file_paths = []
    for i in range(len(pdf_docs)):
        bytes_data = pdf_docs[i].read() 
        # print(pdf_docs[i].name, bytes_data)
        curr_file_path = os.path.join("./tmp", pdf_docs[i].name)
        with open(curr_file_path, "wb") as f:
            f.write(bytes_data)
        file_paths.append(curr_file_path)
    return file_paths

def get_document_chunks(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1500,
        chunk_overlap = 150
    )
    chunks = text_splitter.split_documents(pages)
    print(f'Completed splitting chunks')
    return chunks

# def get_text_chunks(text):
#     text_splitter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size=1000,
#         chunk_overlap=200,
#         length_function=len
#     )
#     chunks = text_splitter.split_text(text)
#     print(f'Completed splitting chunks')
#     return chunks


def get_vectorstore(text_chunks):
    embeddings = OllamaEmbeddings()
    persist_directory = 'docs/chroma/'
    print(f'Starting storing chunks as embeddings into vector DB')
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    # vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    shutil.rmtree(persist_directory)
    vectorstore = Chroma.from_documents(
        documents=text_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f'Completed storing chunks in vector DB')
    return vectorstore


def get_conversation_chain(vectorstore, model_option):
    llm = ChatOllama(model=model_option, temperature=0)
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

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


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Upload your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", type=['pdf', 'txt', 'docx'], accept_multiple_files=True)
    
        st.subheader("Choose Model")
        model_option = st.radio("Choose your model:",('llama2', 'mistral'))
        st.write("You selected the model:", model_option)
        if st.button("Process"):
            with st.spinner("Processing"):
                file_paths = save_file_to_tmp(pdf_docs)
                # get pdf text
                # raw_text = get_pdf_text(pdf_docs)
                raw_text = get_pypdf_text(file_paths)

                # get the text chunks
                text_chunks = get_document_chunks(raw_text)
                # text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore,
                    model_option)


if __name__ == '__main__':
    main()