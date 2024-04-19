## SECTION 1 : PROJECT TITLE
## GURUDOCS: CHATBOT FOR QUERYING DOCUMENTS USING RAG and LLM


---


## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT

![gurudocs example](images/example.png)


---

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID (MTech Applicable)  | Work Items (Who Did What) |
| :------------ |:---------------:| :-----| 
| Alvin Wong Ann Ying | A0266486M | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| 
| Brandon Chua Hong Huei | A0168608U | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz| 
| Ong Si Ci | A0266450E | xxxxxxxxxx yyyyyyyyyy zzzzzzzzzz|


---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

---

## SECTION 5 : USER GUIDE

`Refer to appendix <Installation & User Guide> in project report at Github Folder: ProjectReport`

### Local Installation

- Python 3.10
- Ollama (see download instructions [here](https://ollama.com/download))
- NodeJS v18.20.1

```
conda create -n gurudocs python=3.10 -y
conda activate gurudocs
pip install -r requirements.txt
ollama pull llama2
ollama pull mistral 
```
### Start Application

```
python main.py
cd frontend/
npm start
```

Once you have started the application, your webpage should automatically pop up. You can then upload your PDF documents and chat with GuruDocs!


### Troubleshoot

If you are facing issues with ```npm start```, try to run the following to troubleshoot. This will perform a fresh installation of node modules required. 

```
cd frontend/
rm -rf node_modules
npm install
```

---
## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`