import { useState } from "react"
import axios from "axios"
import Score from "../components/Score"

export default function Analyze(){

const [file,setFile] = useState(null)
const [job,setJob] = useState("")
const [result,setResult] = useState(null)

const submit = async()=>{

const formData = new FormData()

formData.append("resume",file)
formData.append("job_description",job)

const res = await axios.post(
"https://ai-resume-analyzer-production-4363.up.railway.app/analyze",
formData
)

setResult(res.data)

}

return(

<div style={{padding:"40px"}}>

<h1>AI Resume Analyzer</h1>

<input
type="file"
onChange={(e)=>setFile(e.target.files[0])}
/>

<br/><br/>

<textarea
rows="8"
cols="60"
placeholder="Paste Job Description"
onChange={(e)=>setJob(e.target.value)}
/>

<br/><br/>

<button onClick={submit}>
Analyze Resume
</button>

{result && (

<div style={{marginTop:"40px"}}>

<Score score={result.ats_score} />

<h2>Resume Skills</h2>

{result.resume_skills.map((s,i)=>(
<span key={i} style={{marginRight:"10px"}}>
{s}
</span>
))}

<h2>Missing Skills</h2>

{result.missing_skills.map((s,i)=>(
<span key={i} style={{color:"red",marginRight:"10px"}}>
{s}
</span>
))}

<h2>Strengths</h2>

<ul>
{result.strengths.map((s,i)=>(
<li key={i}>{s}</li>
))}
</ul>

<h2>Improvements</h2>

<ul>
{result.improvements.map((s,i)=>(
<li key={i}>{s}</li>
))}
</ul>

</div>

)}

</div>

)

}