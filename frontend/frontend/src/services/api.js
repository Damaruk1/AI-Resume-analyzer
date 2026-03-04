import axios from "axios"

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
})

export const analyzeResume = (formData) =>
  API.post("/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })

export const getHistory = () => API.get("/history")