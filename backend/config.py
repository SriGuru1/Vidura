# Stores config var
import os
from dotenv import load_dotenv

#loading env var
load_dotenv()

# Getting OPENAI API KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Embedding model for generating vector embeddings
EMBEDDING_MODEL = "text-embedding-3-small"

#LLM Model for generating ans
LLM_MODEL = "gpt-3.5-turbo"

