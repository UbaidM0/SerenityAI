# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import LanceDB
# from dotenv import load_dotenv
# import os
# import pdfplumber

# # extract
# def extract_document_text(pdf_path):
#     text = ""
#     with pdfplumber.open(pdf_path) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text()
#     return text


# # Load environment variables from .env file
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# # Initialize OpenAI embeddings
# embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# # Function to process PDFs and store text and embeddings in LanceDB
# def process_pdf_and_store_in_db(pdf_path, db):
#     # Extract text from PDF
#     text = extract_document_text(pdf_path)
    
#     # Split text into manageable chunks (since OpenAI models have a token limit)
#     chunks = split_text(text, chunk_size=512)  # Example chunk size
    
#     # Generate embeddings for each chunk and store in LanceDB
#     for chunk in chunks:
#         embedding = embeddings.embed_text(chunk)
#         db.add_documents([{"embedding": embedding, "content": chunk}])

# # Function to split text into smaller chunks
# def split_text(text, chunk_size=512):
#     words = text.split()
#     chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
#     return chunks

# # Initialize LanceDB (define your path to the LanceDB instance)
# db = LanceDB("path_to_your_lancedb")

# # Path to your PDF document
# pdf_path = "path_to_your_pdf_document.pdf"

# # Process and store the PDF content into the database
# for doc in docs:
#     process_pdf_and_store_in_db(pdf_path, db)

