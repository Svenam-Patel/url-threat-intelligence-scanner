import { useState, useEffect } from "react";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:5000";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState({ total: 0, safe: 0, suspicious: 0 });

  const login = async () => {
    const res = await axios.post("/login", { username, password });
    if (res.data.success) setLoggedIn(true);
    else alert("Invalid login");
  };

  const scan = async () => {
    const res = await axios.post("/scan", { url });
    setResult(res.data);
    fetchHistory();
    fetchStats();
  };

  const fetchHistory = async () => {
    const res = await axios.get("/history");
    setHistory(res.data);
  };

  const fetchStats = async () => {
    const res = await axios.get("/stats");
    setStats(res.data);
  };

  useEffect(() => {
    if (loggedIn) {
      fetchHistory();
      fetchStats();
    }
  }, [loggedIn]);

  if (!loggedIn) {
    return (
      <div>
        <h2>Login</h2>
        <input placeholder="Username" onChange={e => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
        <button onClick={login}>Login</button>
      </div>
    );
  }

  return (
    <div>
      <h1>URL Threat Scanner</h1>

      <input value={url} onChange={e => setUrl(e.target.value)} />
      <button onClick={scan}>Scan</button>

      {result && (
        <div>
          <h3>{result.status}</h3>
          <p>Score: {result.score}</p>
          <ul>
            {result.reasons.map((r, i) => <li key={i}>{r}</li>)}
          </ul>
        </div>
      )}

      <h2>Stats</h2>
      <p>Total: {stats.total}</p>
      <p>Safe: {stats.safe}</p>
      <p>Suspicious: {stats.suspicious}</p>

      <h2>History</h2>
      <table>
        <tbody>
          {history.map((h, i) => (
            <tr key={i}>
              <td>{h.url}</td>
              <td>{h.status}</td>
              <td>{h.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
