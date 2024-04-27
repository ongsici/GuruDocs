## SECTION 1 : PROJECT TITLE
## GURUDOCS: CHATBOT FOR QUERYING DOCUMENTS USING RAG and LLM

![gurudocs example](images/example.png)


---


## SECTION 2 : EXECUTIVE SUMMARY 

GuruDocs is a free chatbot designed to enhance the efficiency of information retrieval from lengthy policy and/or regulatory documents.  Leveraging Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs), GuruDocs offers context-aware search results, thus improving user experience and productivity. This project addresses the limitations of keyword-based search systems and the challenges in fine-tuning LLMs for specific document queries. 

---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) |
| :------------ |:---------------:| :-----| 
| Alvin Wong Ann Ying | A0266486M | <ul><li>Created modified version of RAGAs evaluation library that does not require OpenAI API key</li><li>Implemented end-to-end evaluation workflow</li></ul>| 
| Brandon Chua Hong Huei | A0168608U | <ul><li>Designed and implemented RAG components</li><li>Experimented with various RAG components to optimise GuruDocs performance</li></ul>| 
| Ong Si Ci | A0266450E | <ul><li>Project lead/manager</li><li>Frontend and backend development</li></ul><ul><li>Initial prototype of RAG components</li><li>Dockerisation of product for deployment</li></ul>|


---

## SECTION 4 : SYSTEM ARCHITECTURE & USE CASE DEMO

![gurudocs architecture](images/architecture.png)

![demo](https://youtu.be/Pukb5Xa0ToQ)

---

## SECTION 5 : USER GUIDE

`Refer to appendix <Installation & User Guide> in project report at Github Folder: ProjectReport`

First, install Ollama. See download instructions [here](https://ollama.com/download)

```
git clone
cd GuruDocs/
ollama pull llama2
ollama pull mistral 
```

### 5.1 [Recommended] Docker Installation

Prerequisites:
- Docker 
- Nvidia container toolkit (for running Docker with GPU)

```
chmod +x ./docker_build.sh
./docker_build.sh
```

#### Start Application

```
chmod +x ./gurudocs.sh
./gurudocs.sh start
./gurudocs.sh stop
```
Once you have started the application, your webpage should automatically pop up. You can then upload your PDF documents and chat with GuruDocs!

### 5.2 Local Installation

- Python 3.10
- NodeJS v18.20.1

```
conda create -n gurudocs python=3.10 -y
conda activate gurudocs
pip install -r requirements.txt
```
##### Start Application

You will need to start both the frontend and backend using the following codes:

```
python main.py
cd frontend/
npm start
```

##### Troubleshoot

If you are facing issues with ```npm start```, try to run the following to troubleshoot. This will perform a fresh installation of node modules required. 

```
cd frontend/
rm -rf node_modules
npm install
```

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`