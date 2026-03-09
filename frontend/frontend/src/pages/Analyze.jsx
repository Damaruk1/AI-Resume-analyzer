import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

export default function Analyze() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!resumeFile) {
      alert("Upload a resume");
      return;
    }

    const formData = new FormData();
    formData.append("file", resumeFile);
    formData.append("job_description", jobDescription);

    try {
      setLoading(true);

      const res = await axios.post(
        "https://ai-resume-analyzer-production-4363.up.railway.app/analyze",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );

      setResult(res.data);
      setLoading(false);
    } catch (err) {
      console.error(err);
      alert("Analysis failed");
      setLoading(false);
    }
  };

  return (
    <div style={container}>
      <h1>AI Resume Analyzer</h1>

      <div style={card}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setResumeFile(e.target.files[0])}
        />

        <textarea
          placeholder="Paste job description..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />

        <button onClick={analyzeResume}>Analyze Resume</button>
      </div>

      {loading && <p>Analyzing resume...</p>}

      {result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={resultCard}>
          
          <h2>ATS Score</h2>

          <div style={progressBar}>
            <div
              style={{
                ...progressFill,
                width: `${result.score}%`,
              }}
            />
          </div>

          <p>{result.score}% Match</p>

          <h3>Skills Found</h3>
          <ul>
            {result.skills_found?.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

          <h3>Missing Skills</h3>
          <ul>
            {result.missing_skills?.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>

          <h3>Strengths</h3>
          <p>{result.strengths}</p>

          <h3>Improvements</h3>
          <p>{result.improvements}</p>
        </motion.div>
      )}
    </div>
  );
}

const container = {
  minHeight: "100vh",
  background: "#0f172a",
  color: "white",
  padding: "40px",
  textAlign: "center",
};

const card = {
  background: "#1e293b",
  padding: "20px",
  borderRadius: "10px",
  margin: "20px auto",
  width: "400px",
  display: "flex",
  flexDirection: "column",
  gap: "10px",
};

const resultCard = {
  background: "#1e293b",
  padding: "25px",
  marginTop: "30px",
  borderRadius: "10px",
  width: "500px",
  marginLeft: "auto",
  marginRight: "auto",
};

const progressBar = {
  width: "100%",
  height: "20px",
  background: "#334155",
  borderRadius: "10px",
  overflow: "hidden",
};

const progressFill = {
  height: "100%",
  background: "#22c55e",
};