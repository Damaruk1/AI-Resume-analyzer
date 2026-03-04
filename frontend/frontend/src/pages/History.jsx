import { useEffect,useState } from "react"
import { getHistory } from "../services/api"

function History(){

const [data,setData]=useState([])

useEffect(()=>{

getHistory().then(res=>setData(res.data))

},[])

return(

<div style={{padding:"40px"}}>

<h2>Analysis History</h2>

{data.map((item,i)=>(

<div key={i} style={{marginBottom:"20px"}}>

<p>Score: {item.match_score}</p>

<p>
Missing Skills: {item.missing_skills.join(", ")}
</p>

</div>

))}

</div>

)

}

export default History