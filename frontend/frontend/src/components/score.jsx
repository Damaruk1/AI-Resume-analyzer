import GaugeChart from "react-gauge-chart"

export default function Score({score}) {

return (

<div style={{width:"350px",margin:"20px auto"}}>

<GaugeChart
id="ats-score"
nrOfLevels={20}
percent={score/100}
/>

<h2 style={{textAlign:"center"}}>
ATS Score: {score}%
</h2>

</div>

)

}