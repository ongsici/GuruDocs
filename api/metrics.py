from sentence_transformers import SentenceTransformer, util
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
import subprocess
import pandas as pd

# Load the pre-trained Sentence Transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Function to evaluate how faithful the response is against the retreived context. Currently Threshold = 80%
def faithfulness(response, contexts):
    
    # Tokenize response into sentences
    response_sentences = sent_tokenize(response)

    valid_statements = []
    # Iterate through each response sentence
    for sentence in response_sentences:
        for context in contexts:
            # Calculate similarity score with each context sentence
            similarity_scores = util.cos_sim(model.encode(sentence), model.encode(context))
            if similarity_scores>= 0.8:
                # print(similarity_scores,context)
                valid_statements.append(sentence)
    
    # Calculate faithfulness score
    faithfulness_score = len(valid_statements) / len(response_sentences)
    if faithfulness_score >= 1.0:
        faithfulness_score = 1.0
    print("Faithfulness Score:", faithfulness_score)
    return faithfulness_score

# Function to generate hypothetical questions from the responses. 
def generate_questions(response, model_option):
    
    # Define the prompt input
    prompt = f" generate possible questions based solely on this response {response}"

    # Execute the command and capture the output
    result = subprocess.run(["ollama", "run", model_option], input=prompt, text=True, capture_output=True)

    # Extract and format the generated questions
    generated_questions = result.stdout.strip().split("\n")
    formatted_questions = [question.split('.')[-1] for question in generated_questions if '?' in question]

    return formatted_questions

# Function to compute how relevance is the generated QN is related to the actual query through reversed - engineering from the responses. 
def answer_relevancy(query, generated_QN):
    
    # Convert the query and Hypo-generated questions into embeddings
    query_embedding = model.encode(query)
    generated_QN_embeddings = model.encode(generated_QN)

    # Compute cosine similarity between the query and each Hypo-generated question
    similarity_scores = util.cos_sim([query_embedding], generated_QN_embeddings)[0]
    # print(f"Listing all the similarity_scores: {similarity_scores}")

    # Compute the average similarity score for Hypo-generated questions
    avg_similarity_score = np.mean(similarity_scores.tolist())

    # Print the average similarity scores
    print("Answer Relevancy Score:", avg_similarity_score)
    return avg_similarity_score

# Function to compute how precise the context is in relation to the retrieved contexts
def context_precision(ground_truth, contexts):
    # Initialize the valid count
    valid_count = 0

    # Encode the ground truth
    ground_truth_embedding = model.encode([ground_truth]) 

    # Iterate through each context
    for context in contexts:
        # Encode the context
        context_embedding = model.encode([context])

        # Calculate cosine similarity between context and ground truth
        similarity_score = util.cos_sim(ground_truth_embedding, context_embedding)[0][0]
        valid_count += similarity_score
    
    # print(f"Overall score attained: {valid_count.item()}")

    precision_score = valid_count / len(contexts)
    print(f"Context precision score = {precision_score.item()}")
    return precision_score.item()

# Function to evaluate how relevant the retrieved context is against the actual response
def context_recall(ground_truth, contexts):
    # Tokenize ground truth into sentences
    GT = sent_tokenize(ground_truth)

    valid_context = []
    # Iterate through each response sentence
    for sentence in GT:
        for context in contexts:
            # Calculate similarity score with each context sentence
            similarity_scores = util.cos_sim(model.encode(sentence), model.encode(context))
            if similarity_scores >= 0.5:
                print(similarity_scores, context)
                valid_context.append(context)

    # print(f"No. of Valid Statements: {len(valid_context)}")

    # Calculate context recall score
    context_recall_score = len(valid_context) / len(contexts)
    print("Context Recall Score:", context_recall_score)

    return context_recall_score


