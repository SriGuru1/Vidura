from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
from sentence_transformers import SentenceTransformer
import re
import faiss
import numpy as np
from config import GROQ_API_KEY, EMBEDDING_MODEL, LLM_MODEL

# Initializing Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Initializing Embedding Model
embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# 1. Extracting YT Video ID (check & return video id)
def extract_video_id(url):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        # if we find a match
        if match:
            return match.group(1)
    return None


# 2. Fetching Video Transcript (video id -> full transcript text)
def get_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()
        try:
            # fetch english transcript
            transcript_data = ytt_api.fetch(video_id, languages=["en"])
        except Exception:
            transcript_list = ytt_api.list(video_id)
            transcript_data = next(iter(transcript_list)).fetch()

        full_text = " ".join(item.text for item in transcript_data)
        return re.sub(r"\s+", " ", full_text)

    except Exception as e:
        print("Transcript error: ", e)
        return None
    

# 3. Splitting Transcript into Chunks (Full transcript -> split it into smaller chunks)
def split_text(text, chunk_size=150):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])  
        for i in range(0, len(words), chunk_size)
    ]


# 4. Creating Embeddings (create embeddings from chunks: text chunk -> embedding vector)
def create_embeddings(text_list):
    embeddings = embedding_model.encode(text_list)
    return np.array(embeddings).astype("float32")


# 5. Building FAISS Index (store embeddings -> (in) -> Vector -> search)
# FAISS - fast similarity search on vectors
def build_faiss_index(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape[1])      #Create FAISS Index
    index.add(embeddings)       # adding the embeddings to the index
    return index  # return the index


# 6. Retrieving Relevant Chunks (search: FAISS index -> return: most relevant chunks for a user query)
def retrieve_chunks(index, query_embedding, k=3):
    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"), k
    )
    return indices[0]


# 7. Asking LLM (send: retrieved transcript context & user que -> LLM model)
def ask_llm(context, question):
    if not context.strip():
        return "Sorry, I couldn't find relevant information in the video transcript"
    # Truncate context
    context = context[:6000]

    prompt = f""" You are an AI assistant answering question about a YouTube video. 
    The transcript may be in any language (Kannada, Hindi, English, etc).
    Always answer in English using the provided context.

    Transcript Context:
    {context}

    Question:
    {question}

    Answer clearly in English: """

    # calling LLM API
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
           {"role": "system", "content": "You answer questions about YouTube videos."},
           {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content