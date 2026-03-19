#file -> runs the FastAPI backend
from fastapi import FastAPI

from rag_utils import *
from rag_utils import extract_video_id

from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI App
app = FastAPI()

# middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage
chunks = []
index = None


# 1. Video Process Endpoint
@app.post("/process_video")
def process_video(url: str):
    global chunks, index

    # Extract video ID safely
    video_id = extract_video_id(url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    
    # Get Transcript
    text = get_transcript(video_id)
    if text is None:
        return {"error": "Transcript not available for this video"}
    
    # Split transcript into chunks
    chunks = split_text(text)

    # Create embeddings
    embeddings = create_embeddings(chunks)

    # Build FAISS Index
    index = build_faiss_index(embeddings)

    return {"message": "Video processed successfully"}


# 2. Question Endpoint
@app.post("/ask")
def ask(question: str):
    if index is None:
        return {"error": "Please process a video first"}
    
    try: 
        # Convert: que -> embedding
        query_embedding = create_embeddings([question])[0]

        # Retrieve Relevant Chunks
        top_chunks = retrieve_chunks(index, query_embedding)
        if len(top_chunks) == 0:
            return {"answer": "No relevant context found in the video."}
        
        # Combine Context
        context_chunks = []
        for i in top_chunks:
            if i < len(chunks):
                context_chunks.append(chunks[i])

        context = " ".join(context_chunks)

        print("Retrieved chunks: ", top_chunks)     #debug
        print("Context preview: ", context[:300])

        # Ask LLM
        answer = ask_llm(context, question)
        # Return ans
        return {"answer": answer}

    except Exception as e:
        print("Ask error: ", e)
        return {"error", str(e)}

    
    