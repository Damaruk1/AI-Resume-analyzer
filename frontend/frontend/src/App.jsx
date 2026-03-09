import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Analyze from "./pages/Analyze";
import History from "./pages/History";

export default function App() {
  return (
    <Router>
      <div className="app-container">

        <nav className="navbar">
          <h2 className="logo">AI Resume Analyzer</h2>

          <div className="nav-links">
            <Link to="/">Dashboard</Link>
            <Link to="/analyze">Analyze Resume</Link>
            <Link to="/history">History</Link>
          </div>
        </nav>

        <div className="content">
          <Routes>
            <Route path="/" element={<Analyze />} />
            <Route path="/analyze" element={<Analyze />} />
            <Route path="/history" element={<History />} />
          </Routes>
        </div>

      </div>
    </Router>
  );
}