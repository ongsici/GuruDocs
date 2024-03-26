import streamlit as st
from htmlTemplates import css, bot_template, user_template
import os
from api.llm_utils import get_conversation_chain, get_document_chunks, get_pypdf_text, get_vectorstore, get_summary
import glob

def save_file_to_tmp(pdf_docs):
    file_paths = []
    tmp_dir = "./tmp"
    os.makedirs(tmp_dir, exist_ok=True)
    print(f'tmp dir created')

    #cleanup 
    prev_files = glob.glob(f'{tmp_dir}/*')
    for f in prev_files:
        if os.path.isfile(f):
            os.remove(f) 

    for i in range(len(pdf_docs)):
        bytes_data = pdf_docs[i].read() 
        curr_file_path = os.path.join(tmp_dir, pdf_docs[i].name)
        with open(curr_file_path, "wb") as f:
            f.write(bytes_data)
        file_paths.append(curr_file_path)
    return file_paths


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

    st.header("Welcome to GuruDocs! :books:")

    # TODO: add document(s) summary from LLM
    st.subheader("Summary")
    st.write(f'Document summary here')

    st.subheader("Chat with your documents:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    # TODO: create console to show background process status 

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
                raw_text = get_pypdf_text(file_paths)

                # get summary
                summary = get_summary(raw_text, model_option)
                # TODO: add document(s) summary from LLM
                st.subheader("Summary")
                st.write(f'Document summary here {summary}')

                # get the text chunks
                text_chunks = get_document_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore,
                    model_option)


if __name__ == '__main__':
    main()