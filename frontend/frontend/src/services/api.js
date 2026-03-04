import axios from "axios"

const API = axios.create({
  baseURL: "https://ai-resume-analyzer-production-4363.up.railway.app"
})

export const analyzeResume = (formData) =>
  API.post("/analyze", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  })

export const getHistory = () => API.get("/history")
