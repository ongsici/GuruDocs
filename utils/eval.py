import os
import nltk
import uuid
import csv
import re
import argparse

from langchain_community.document_loaders.pdf import PyPDFLoader  
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from api.metrics import context_precision, context_recall, faithfulness, generate_questions, answer_relevancy

# Initialize lists using a for loop
vectorstore_uuid_list = []
vectorstore_dict, conversation_chain_store, pages_store = ({} for _ in range(3))
count = 0

# Define the argument parser
parser = argparse.ArgumentParser(description='Process file paths for Q&A evaluation.')
parser.add_argument('--pdf_paths', nargs='+', default=["/home/mraway/Desktop/src/QA_Summary/PDFs/NTUC.pdf"],
                    help='List of file paths for the PDF documents.')
parser.add_argument('--query_file', default='sample_NTUC.txt',
                    help='File path for the evaluation queries with ground truths provided.')
parser.add_argument('--persist_directory', default='docs/chroma/',
                    help='Directory path for persistence of vectorstore data.')
parser.add_argument('--output_path', default='output.csv',
                    help='File path to save the evaluation results.')

# Parse the arguments
args = parser.parse_args()

class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

def clean_chunk_text(text):
    # Define translation table to remove specified characters
    translation_table = str.maketrans('', '', '\n$#@^*()<>{}\\|-_…/')
    # Remove specified characters from text
    cleaned_text = text.translate(translation_table)
    return cleaned_text


def get_document_chunks(file_paths):
    all_chunks = []
    for file_path in file_paths:
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
                # Check if the length of the cleaned sentence is less than or equal to 10
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

    store = {}
    
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

# Define a function to read the text file and extract question-answer pairs
def read_text_file(file_path):
    qa_pairs = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Split each line into question and answer
            question, answer = line.strip().split(' - ')
            # Append the question-answer pair to the list
            qa_pairs.append({'question': question, 'answer': answer})
    return qa_pairs

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

# Example usage which access the arguments
file_paths = args.pdf_paths
query_file = args.query_file
persist_directory = args.persist_directory
output_path = args.output_path

#Get Q&A Pairs
qa_pairs = read_text_file(query_file)
queries = [qa['question'] for qa in qa_pairs]
answer = [qa['answer'] for qa in qa_pairs]

#Models to be used for evaluation
models = ['mistral', 'llama2']

# Get document chunks
chunks = get_document_chunks(file_paths)

# Get vectorstore
vectorstore = get_vectorstore(chunks, persist_directory)
vectorstore_uuid = str(uuid.uuid4())
vectorstore_dict[vectorstore_uuid] = vectorstore
vectorstore_uuid_list.append(vectorstore_uuid)
print(vectorstore_uuid_list)

# Open CSV file for saving the evaluation results. Refplace the filepath and filednames for yourself with the models you want to evaluate i.e. Llama3
with open(output_path, mode='w', newline='') as csv_file:
    fieldnames = ['User Query', 'Answer', 
                  'Mistral_Prompt', 'Mistral_Faithfulness', 'Mistral_Answer_Relevancy', 'Mistral_Precision', 'Mistral_Recall', 
                  'Llama2_Prompt', 'llama2_Faithfulness', 'L2_Answer_Relevancy', 'Llama2_Precision', 'Llama2_Recall']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    for query, ans in zip(queries, answer):
        count += 1
        # Initialize empty dictionary to store row data
        row_data = {'User Query': query, 'Answer': ans}  # Assign query and answer to respective columns
        for modeloption in models:
            print(f'Staring to process Qn {count} with {modeloption}.')
            conversation_rag, context = conversational_rag_chain(vectorstore_dict[vectorstore_uuid], modeloption, query)
            response = conversation_rag.invoke({"input":query},config={"configurable":{"session_id":'SampleSection'}},)["answer"]
            faithful_Score, Ans_Relevancy_Score = eval(query,response,context,modeloption)
            precision_scores = context_precision(ans, response) 
            recall_scores = context_recall(ans, response)
            if modeloption == 'mistral':
                row_data['Mistral_Prompt'] = response
                row_data['Mistral_Faithfulness'] = faithful_Score
                row_data['Mistral_Answer_Relevancy'] = Ans_Relevancy_Score
                row_data['Mistral_Precision'] = precision_scores
                row_data['Mistral_Recall'] = recall_scores
            elif modeloption == 'llama2':
                row_data['Llama2_Prompt'] = response
                row_data['llama2_Faithfulness'] = faithful_Score
                row_data['L2_Answer_Relevancy'] = Ans_Relevancy_Score
                row_data['Llama2_Precision'] = precision_scores
                row_data['Llama2_Recall'] = recall_scores
         # Write row to CSV
        writer.writerow(row_data)

print(f"Data has been saved to {output_path}")