import { useEffect, useState } from "react";
import axios from "axios";

export default function History() {

  const [history,setHistory] = useState([]);

  useEffect(()=>{

    axios.get("https://ai-resume-analyzer-production-4363.up.railway.app/history")
    .then(res => setHistory(res.data));

  },[]);

  return (

    <div>

      <h1>Analysis History</h1>

      {history.map((item,i)=>(
        <div className="card" key={i}>

          <h3>ATS Score: {item.score}</h3>

          <p>
            <strong>Missing Skills:</strong>{" "}
            {item.missing_skills?.join(", ")}
          </p>

          <p><strong>Strengths:</strong> {item.strengths}</p>

          <p><strong>Improvements:</strong> {item.improvements}</p>

        </div>
      ))}

    </div>
  )
}