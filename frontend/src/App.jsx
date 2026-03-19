import { useState } from "react";
import { processVideo, askQuestion } from "./api"

function App() {
  // for YT URL
  const [url, setUrl] = useState("")

  //for User Que
  const [question, setQuestion] = useState("")

  // chat history state (que & ans)
  const [chat, setChat] = useState([])

  // loading state for API calls
  const [loading, setLoading] = useState(false)

  // fun: to Process video (send the yt url to backend for processing)
  const handleProcess = async() => {
    // check if url is entered
    if (!url) {
      alert("Enter YouTube URL")
      return
    }
    
    setLoading(true)

    try{
      // Calling Backend API to Process video
      await processVideo(url)
      alert("Video processed successfully")
    }

    catch {
      alert("Error processing video")
    }

    setLoading(false)
  }

  // Fun: Ask Que about processed video
  const handleAsk = async() => {

    // Do nothing if no que
    if (!question) return

    setLoading(true)

    // Add new Q&A to chat history
    try {
      const res = await askQuestion(question)

      // Add new Q&A to chat history
      setChat([
        ...chat,
        {
          q: question,
          a: res.data.answer || res.data.error || "No answer received"
        }
      ])

      //Clear input box after asking
      setQuestion(" ")
    }

    catch{
      alert("Error getting answer")
    }

    setLoading(false)
    
  }


return (
  // Main container
  <div className="min-h-screen bg-gray-100 flex justify-center p-6">
    {/* Chatbot section */}
     <div className="w-full max-w-3xl bg-white shadow-lg rounded-xl p-6">
      <h1 className="text-2xl font-bold text-center mb-6">
        YouTube RAG Chatbot
      </h1>
      {/* Section to enter YT URL */}
      <div className="flex gap-3 mb-6">
        <input 
          type="text" 
          placeholder="Paste Your URL"
          value={url}
          onChange={(e)=>setUrl(e.target.value)} 
          className="flex-1 border p-2 rounded"
        />

        <button onClick={handleProcess}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          {loading ? "Processing Video..." : "Process"}
        </button>
      </div>

      {/* Sectin to ask que */}
      <div className="flex gap-3 mb-6">
        <input 
          type="text" 
          placeholder="Ask question about the video"
          value={question}
          onChange={(e)=>setQuestion(e.target.value)} 
          className="flex-1 border p-2 rounded"
        />
        <button
          onClick={handleAsk}
          disabled={loading}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>

      {/* Chat display Section */}
      <div className="space-y-4 max-h-[400px] overflow-y-auto">
        {chat.map((c, i) => (
          <div key={i} className="border rounded p-4">

            {/* User question */}
            <p className="font-semibold text-gray-700">
              You: {c.q}
            </p>
            <p className="text-blue-600 mt-2">
              AI: {c.a}
            </p>
          </div>
        ))}
      </div>
    </div>
  </div>
)
}

export default App