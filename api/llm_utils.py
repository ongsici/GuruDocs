
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
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

import os
import pandas as pd
import re
import nltk
from api.metrics import faithfulness, generate_questions, answer_relevancy

class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

def get_pypdf_text(file_path):
    loader = PyPDFLoader(os.path.abspath(file_path))
    pages = loader.load()
    return pages

def clean_chunk_text(text):
    # Define translation table to remove specified characters
    translation_table = str.maketrans('', '', '\n$#@^*()<>{}\\|-_…/')
    # Remove specified characters from text
    cleaned_text = text.translate(translation_table)
    return cleaned_text

def get_document_chunks(file_path):
    all_chunks = []
    
    loader = PyPDFLoader(os.path.abspath(file_path))
    pages = loader.load()
    # Iterate over pages
    for page_num, page in enumerate(pages, start=1):
        # Get the text content of the page
        page_content = page.page_content
        # Split page content into sentences
        sentences = nltk.sent_tokenize(page_content)
        # Append each sentence as a chunk along with metadata
        for i, sentence in enumerate(sentences):
            metadata = {'source': page.metadata['source'], 'page': page_num}
            chunk = {'content': sentence.strip(), 'metadata': metadata}
            # Clean the text of the chunk
            chunk['content'] = clean_chunk_text(chunk['content'])
            # remove cleaned sentence if less than or equal to 10
            if len(chunk['content']) > 10:
                all_chunks.append(chunk)
    print(f'Completed splitting chunks')
    return all_chunks

def get_embedding():
    model_name = "BAAI/bge-small-en"
    model_kwargs = {"device": "cuda"}
    encode_kwargs = {"normalize_embeddings": True}
    hf_embd = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
    return hf_embd

def get_vectorstore(text_chunks, persist_directory):
    embeddings = get_embedding()
    
    print(f'Starting storing chunks as embeddings into vector DB')
    
    # Convert text_chunks into Document objects
    documents = [Document(page_content=chunk['content'], metadata=chunk['metadata']) for chunk in text_chunks]
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f'Completed storing chunks in vector DB')
    return vectorstore


def get_conversation_chain(vectorstore, model_option, query):
    llm = ChatOllama(model=model_option, temperature=0)

    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
        )
    retriever = vectorstore.as_retriever(search_type='mmr')
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever= retriever,
        memory=memory
    )
    context = retriever.get_relevant_documents(query)
    return conversation_chain, context

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

def conversational_rag_chain(vectorstore,model_option,query):
    llm = ChatOllama(model=model_option, temperature=0)

    retriever = vectorstore.as_retriever()
    context = retriever.get_relevant_documents(query)
    
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_system_prompt = """You are an AI assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


    store = {}

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return conversational_rag_chain, context

def split_into_sentences(text):
    sentences = []
    for element in text:
        element = element.replace('\n', ' ').strip()
        sentence_endings = r'[.!?]'
        element_sentences = re.split(sentence_endings, element)
        element_sentences = [re.sub(r'\s+', ' ', sentence.strip()) for sentence in element_sentences if sentence.strip()]
        sentences.extend(element_sentences)
    return sentences

def eval(query,answer,context,model_option):
    page_contents = [doc.page_content for doc in context]
    output = split_into_sentences(page_contents)
    score_faithfulness = faithfulness(answer,output)

    predicted_Qn = generate_questions(answer,model_option)
    score_Ans_Relevancy = answer_relevancy(query,predicted_Qn)
    return score_faithfulness, score_Ans_Relevancy
