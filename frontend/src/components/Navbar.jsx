import { Link } from "react-router";
import "./Navbar.css";

export default function Navbar() {
  return (
    <>
    <header className="navbar">
        <div className="navbar-left">
        <div className="logo">
          <div className="logo-icon">👤</div>
          <span className="logo-text">Senior Checkin</span>
        </div>
        </div>
        
      <nav className="navbar-right">
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/explained">How it works</Link>
        <Link to="/signup">Signup</Link>
      </nav>
    </header>

    </>
  );
}
