import { useState, useEffect } from "react"
import axios from "axios"
import "./App.css"

function App(){

 const [url,setUrl] = useState("")
 const [result,setResult] = useState(null)
 const [history,setHistory] = useState([])

 const scan = async()=>{

   const res = await axios.post(
     "http://127.0.0.1:5000/scan",
     {url}
   )

   setResult(res.data)
   fetchHistory()
 }

 const fetchHistory = async()=>{

   const res = await axios.get(
     "http://127.0.0.1:5000/history"
   )

   setHistory(res.data)
 }

 useEffect(()=>{
   fetchHistory()
 },[])

 return(

 <div className="container">

 <h1>URL Threat Intelligence Scanner</h1>

 <div className="scan-box">
 <input
  placeholder="Enter suspicious URL"
  value={url}
  onChange={(e)=>setUrl(e.target.value)}
 />

 <button onClick={scan}>Scan</button>
 </div>

 {result && (

  <div className="result">

  <h2>Status: {result.status}</h2>

  {result.score !== undefined && (
    <p>Risk Score: {result.score}</p>
  )}

  <ul>

   {result.reasons.map((r,i)=>(
    <li key={i}>{r}</li>
   ))}

  </ul>

  </div>

 )}

 <h2>Scan History</h2>

 <table>

 <thead>
  <tr>
   <th>URL</th>
   <th>Score</th>
   <th>Status</th>
  </tr>
 </thead>

 <tbody>

 {history.map(row=>(
  <tr key={row[0]}>
   <td>{row[1]}</td>
   <td>{row[2]}</td>
   <td>{row[3]}</td>
  </tr>
 ))}

 </tbody>

 </table>

 </div>

 )

}

export default App
