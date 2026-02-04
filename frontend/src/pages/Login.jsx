import { Link } from 'react-router';
import { useState } from 'react';
import './Login.css';

export default function Login() {
  const [phone, setPhone] = useState('');
  return (
    <>
      <div className="login-page">
        <div className="login-container">
          <h1 className="login-title">Welcome Back</h1>
          <p className="login-subtitle">Enter your phone number to log in.</p>

          <form className="login-form">
            <label className="login-label" htmlFor="phone">
              Phone Number
            </label>
            <div className="input-wrap">
              <input
                id="phone"
                className="login-input"
                type="tel"
                placeholder="📱 12 345 678"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
            </div>

            <p className="login-magic">
              ℹ️ We will text you a magic link to log in.
            </p>

            <button className="login-button" type="button">
              SEND LINK ➡️
            </button>
          </form>

          <Link className="login-signup" to="/signup">
            Need help logging in?
          </Link>
        </div>
      </div>
    </>
  );
}
