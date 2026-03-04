import { useState } from "react"
import { analyzeResume } from "../services/api"

function Analyze(){

const [file,setFile]=useState(null)
const [jobDescription,setJobDescription]=useState("")
const [result,setResult]=useState(null)

const handleAnalyze = async()=>{

const formData = new FormData()

formData.append("file",file)
formData.append("job_description",jobDescription)

const res = await analyzeResume(formData)

setResult(res.data)

}

return(

<div style={{padding:"40px"}}>

<h2>Upload Resume</h2>

<input
type="file"
accept=".pdf"
onChange={(e)=>setFile(e.target.files[0])}
/>

<h3>Job Description</h3>

<textarea
rows="6"
cols="60"
value={jobDescription}
onChange={(e)=>setJobDescription(e.target.value)}
/>

<br/><br/>

<button onClick={handleAnalyze}>
Analyze Resume
</button>

{result && (

<div style={{marginTop:"30px"}}>

<h3>Match Score: {result.match_score}%</h3>

<h4>Missing Skills</h4>

<ul>
{result.missing_skills.map((skill,i)=>(
<li key={i}>{skill}</li>
))}
</ul>

</div>

)}

</div>

)

}

export default Analyze