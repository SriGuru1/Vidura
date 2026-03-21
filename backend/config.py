# Stores config var
import os
from dotenv import load_dotenv

#loading env var
load_dotenv()

# Getting GROQ API KEY
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Embedding model for generating vector embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

#LLM Model for generating ans
LLM_MODEL = "llama-3.1-8b-instant"

