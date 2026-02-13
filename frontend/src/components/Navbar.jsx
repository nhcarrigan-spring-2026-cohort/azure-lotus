import { Link } from 'react-router';
import './Navbar.css';
import { useState } from 'react';
import { useAuthContext } from '../context/AuthContext';

export default function Navbar() {
  const [open, setOpen] = useState(false);

  const { isAuthenticated, logout } = useAuthContext();

  function closeMenu() {
    setOpen(false);
  }
  return (
    <>
      <header className="navbar">
        <div className="navbar-left">
          <div className="logo">
            <div className="logo-icon">👤</div>
            <span className="logo-text">Senior Checkin</span>
          </div>
        </div>

        <button
          className="hamburger"
          type="button"
          aria-label="Toggle navigation menu"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          <span className="hamburger-bar"></span>
          <span className="hamburger-bar"></span>
          <span className="hamburger-bar"></span>
        </button>

        <nav className={`navbar-right ${open ? 'open' : ''}`}>
          <Link to="/" onClick={closeMenu}>
            Home
          </Link>
          <Link to="/about" onClick={closeMenu}>
            About
          </Link>
          <Link to="/explained" onClick={closeMenu}>
            How it works
          </Link>
          {isAuthenticated ? (
            <div className="link-button" onClick={logout}>
              Logout
            </div>
          ) : (
            <>
              <Link to="/Login" onClick={closeMenu}>
                Login
              </Link>
              <Link to="/signup" onClick={closeMenu}>
                Sign up
              </Link>
            </>
          )}
        </nav>
      </header>
    </>
  );
}
