import { useState } from "react";
import axios from "axios";
import GaugeChart from "react-gauge-chart";
import { motion } from "framer-motion";

export default function Analyze() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeResume = async () => {
    if (!resumeFile) {
      alert("Please upload a resume first");
      return;
    }

    const formData = new FormData();
    formData.append("file", resumeFile);
    formData.append("job_description", jobDescription);

    try {
      setLoading(true);

      const response = await axios.post(
        "https://ai-resume-analyzer-production-4363.up.railway.app/analyze",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setResult(response.data);
      setLoading(false);
    } catch (error) {
      console.error(error);
      alert("Error analyzing resume");
      setLoading(false);
    }
  };

  return (
    <div style={containerStyle}>
      <motion.h1
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        style={{ color: "white" }}
      >
        AI Resume Analyzer
      </motion.h1>

      <div style={cardStyle}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setResumeFile(e.target.files[0])}
        />

        <textarea
          placeholder="Paste job description here"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          style={textareaStyle}
        />

        <button onClick={analyzeResume} style={buttonStyle}>
          Analyze Resume
        </button>
      </div>

      {loading && <p style={{ color: "white" }}>Analyzing...</p>}

      {result && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={resultCard}
        >
          <h2>ATS Score</h2>

          <GaugeChart
            id="ats-score"
            nrOfLevels={20}
            percent={result.score / 100}
          />

          <div style={section}>
            <h3>Skills Found</h3>
            <ul>
              {result.skills_found?.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

          <div style={section}>
            <h3>Missing Skills</h3>
            <ul>
              {result.missing_skills?.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>

          <div style={section}>
            <h3>Strengths</h3>
            <p>{result.strengths}</p>
          </div>

          <div style={section}>
            <h3>Improvements</h3>
            <p>{result.improvements}</p>
          </div>
        </motion.div>
      )}
    </div>
  );
}

const containerStyle = {
  minHeight: "100vh",
  background: "linear-gradient(135deg,#0f172a,#1e293b)",
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "40px",
};

const cardStyle = {
  background: "rgba(255,255,255,0.1)",
  backdropFilter: "blur(10px)",
  padding: "30px",
  borderRadius: "12px",
  display: "flex",
  flexDirection: "column",
  gap: "15px",
  width: "400px",
};

const textareaStyle = {
  height: "120px",
};

const buttonStyle = {
  padding: "10px",
  background: "#3b82f6",
  border: "none",
  color: "white",
  cursor: "pointer",
  borderRadius: "6px",
};

const resultCard = {
  marginTop: "30px",
  background: "rgba(255,255,255,0.1)",
  padding: "25px",
  borderRadius: "10px",
  color: "white",
  width: "500px",
};

const section = {
  marginTop: "20px",
};