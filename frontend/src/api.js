import axios from "axios"

// Base URL of backend server
const API = "http://127.0.0.1:8000"

// Fun: Process Video (send YT video url to backend)
export const processVideo = async(url) => {
    return axios.post(`${API}/process_video`, null, {
        params: {url}
    })
}

// Fun: Ans the que (ask que related to processed video)
export const askQuestion = async(question) => {
    return axios.post(`${API}/ask`, null, {
        params: {question}
    })
}