import { NavLink } from 'react-router';
import './Navbar.css';
import { useState } from 'react';
import { useAuthContext } from '../context/AuthContext';
import icon from '../assets/home-icon.png';

export default function Navbar({ type = "dashboard" }) {
  const [open, setOpen] = useState(false);
  const { isAuthenticated, logout } = useAuthContext();
  const closeMenu = () => setOpen(false);

  // 🔹 Define links based on page type
  const navLinks = {
    dashboard: [
      { name: "Alerts", path: "/alerts" },
      { name: "Settings", path: "/settings" },
    ],
    checkin: [
      { name: "Dashboard", path: "/dashboard" },
      { name: "Alerts", path: "/alerts" },
      { name: "Settings", path: "/settings" },
    ],
    settings: [
      { name: "Dashboard", path: "/dashboard" },
      { name: "Alerts", path: "/alerts" },
    ],
    default: [
    { name: "Home", path: "/" },
    { name: "About", path: "/about" },
    
  ],
  };

  return (
    <header className="navbar">
      {/* 🔹 Left Section (Logo) */}
      <div className="navbar-left">
        <div className="logo">
          <img
            className="logo-icon"
            src={icon}
            alt="Home"
            onError={(e) => {
              e.currentTarget.style.display = "none";
              e.currentTarget.parentElement.textContent = "🏠";
            }}
          />
          <span className="logo-text">Senior Check-In</span>
        </div>
      </div>

      {/* 🔹 Hamburger Button */}
      <button
        className="hamburger"
        type="button"
        aria-label="Toggle navigation menu"
        aria-expanded={open}
        onClick={() => setOpen((prev) => !prev)}
      >
        <span className="hamburger-bar"></span>
        <span className="hamburger-bar"></span>
        <span className="hamburger-bar"></span>
      </button>

      {/* 🔹 Right Section (Links) */}
      <nav className={`navbar-right ${open ? "open" : ""}`}>
        {navLinks[type]?.map((link) => (
          <NavLink
            key={link.name}
            to={link.path}
            onClick={closeMenu}
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            {link.name}
          </NavLink>
        ))}

        {/* 🔹 Auth Section */}
        {isAuthenticated ? (
          <div className="link-button" onClick={logout}>
            Logout
          </div>
        ) : (
          <>
            <NavLink to="/login" onClick={closeMenu}>
              Login
            </NavLink>
            <NavLink to="/signup" onClick={closeMenu}>
              Sign Up
            </NavLink>
          </>
        )}
      </nav>
    </header>
  );
}