import { useState } from 'react';
import { Link } from 'react-router';
import './Login.css';
import { useAuthContext } from '../context/AuthContext.jsx';
import { useMutation } from '@tanstack/react-query';
import { loginRequest } from '../api/auth.js';
import { useNavigate, useLocation } from 'react-router';

export default function Login() {
  const [formData, setFormData] = useState({
    email: 'user@example.com',
    password: 'string1234',
  });

  const { loginSuccess } = useAuthContext();

  const navigate = useNavigate();
  const location = useLocation()
  const fromLocation = location.state?.from?.pathname || '/';

  const login = useMutation({
    mutationFn: loginRequest,
    onSuccess: (user) => {
      console.log(`Login successful, ${JSON.stringify(user)}`);
      loginSuccess(user);
      navigate(fromLocation, {replace: true});
    },
    onError: (error) => {
      console.error(`Login failed: ${error.data.detail}`);
      alert(`Login failed: ${error.data.detail}`);
    },
  });

  const handleLogin = async (e) => {
    e.preventDefault();
    await login.mutateAsync({
      email: formData.email,
      password: formData.password,
    });
  };

  return (
    <>
      <div className="login-page">
        <div className="login-container">
          <h1 className="login-title">Welcome Back</h1>
          <p className="login-subtitle">
            Enter your username and password to log in.
          </p>

          <form className="login-form" autoComplete="off">
            <label className="login-label" htmlFor="username">
              Username
            </label>
            <div className="input-wrap">
              <input
                id="username"
                className="login-input"
                type="text"
                placeholder="Enter your username"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                required
              />
            </div>

            <label className="login-label" htmlFor="password">
              Password
            </label>
            <div className="input-wrap">
              <input
                id="password"
                className="login-input"
                type="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                required
              />
            </div>

            <button
              className="login-button"
              type="button"
              onClick={handleLogin}
              disabled={login.isPending}
            >
              LOG IN ➡️
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
