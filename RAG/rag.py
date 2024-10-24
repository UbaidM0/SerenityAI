from langchain.chains import RetrievalQA
from langchain_community.vectorstores import LanceDB
from langchain_community.embeddings import OpenAIEmbeddings
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from pyspark.sql import SparkSession
from pyspark.sql import Row
from databricks.connect import DatabricksSession 

spark = DatabricksSession.builder.getOrCreate()

# Load environment variables
load_dotenv()

# Set up API key for OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
# embeddings = OpenAIEmbeddings(api_key=openai.api_key)

# # Initialize LanceDB (path to your LanceDB instance)
# db = LanceDB("path_to_your_lancedb")

# Retrieve relevant documents based on user input
# def retrieve_context(user_input):
#     user_embedding = embeddings.embed_text(user_input)
#     context = db.similarity_search(user_embedding, k=1)  # Get the most relevant document
#     return context[0]["content"] if context else ""

def summarize_conversation(history_df):
    # Collect the conversation history into a list
    conversation_list = history_df.collect()

    # Generate a summary based on user inputs and AI responses
    summary = []
    for row in conversation_list:
        summary.append(f"User: {row.user_input}\nTherapist: {row.ai_response}")
    
    # Limit the length of the summary to fit within token limits
    # Here, we're simply joining the conversation, but you may implement a more sophisticated summarization logic
    full_summary = "\n".join(summary)
    
    # Check if the summary length exceeds token limits (e.g., 4096 for gpt-3.5-turbo)
    # Adjust this logic based on how you estimate token count
    token_limit = 2000 # Leave some buffer
    if len(full_summary.split()) > token_limit:
        # Truncate the summary to fit within token limit
        prompt = f"Summarize the following conversation history to under 2000 words:\n{full_summary}"
        response = openai.Completion.create(
            model="gpt-4",  # Use 'gpt-4' or 'gpt-3.5-turbo'
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        summarized_text = response.choices[0].text.strip()
    else:
        summarized_text = full_summary

    return summarized_text

# Generate AI therapist response using OpenAI API
def generate_response(user_input):
    # context = retrieve_context(user_input)

    # Get the summarized conversation history
    # Read conversation history from Delta Lake
    history_df = spark.read.format("delta").load("/mnt/delta/conversation_history")

    summarized_history = summarize_conversation(history_df)

    # Prepare the prompt with the summarized history and the new user input
    # prompt = f"You are an AI Therapist helping user's with their mental health. Here is a summarized history of your conversation with the user so far: {summarized_history}\n Here are some general therapy guidelines that may be relevant to the user's most recent response: context\n Give a response to the user discussing their feelings/asking followup questions if needed, and giving advice in the same way that a therapist would.\n Here is the user's most recent response: {user_input}\n"
    
    client = OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an AI Therapist. Your goal is to provide empathetic and supportive responses to users discussing their mental health. Limit your response to less than 150 words."},
            {"role": "user", "content": f"Here is a summarized history of your conversation with the user so far: {summarized_history}\nHere is the user's most recent response: {user_input}"}
        ],
        max_tokens=150,
        temperature=0.7,
        model="gpt-3.5-turbo",
    )
    
    return response.choices[0].message.content

# address session id
def update_conversation_history(user_input, ai_response, session_id):
    # Create a DataFrame with the new conversation entry
    new_entry = [
        Row(session_id=session_id, user_input=user_input, ai_response=ai_response)
    ]
    new_df = spark.createDataFrame(new_entry)

    # Append the new entry to the Delta table
    new_df.write.format("delta").mode("append").save("/mnt/delta/conversation_history")

# Main function to start the conversation
def start_conversation():
    session_id = "session_123"  # Unique session identifier
    print("AI Therapist: Hey, how are you feeling today?")

    while True:
        user_input = input("User: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("AI Therapist: Thank you for the conversation. Take care!")
            break
        
        ai_response = generate_response(user_input)
        print(f"AI Therapist: {ai_response}")
        
        update_conversation_history(user_input, ai_response, session_id)

# Start the conversation
start_conversation()

