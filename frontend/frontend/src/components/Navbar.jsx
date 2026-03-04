import { Link } from "react-router-dom"

function Navbar(){

return(

<div style={{
display:"flex",
gap:"30px",
padding:"20px",
background:"#111",
color:"white"
}}>

<Link to="/" style={{color:"white"}}>Dashboard</Link>
<Link to="/analyze" style={{color:"white"}}>Analyze Resume</Link>
<Link to="/history" style={{color:"white"}}>History</Link>

</div>

)

}

export default Navbar