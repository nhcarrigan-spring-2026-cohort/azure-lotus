import { Link } from 'react-router';
import './Login.css';
import { useAuthContext } from '../context/AuthContext.jsx';

export default function Login() {
  const { login } = useAuthContext();

  const handleLogin = async (e) => {
    e.preventDefault();
    await login.mutateAsync({
      email: 'user@example.com',
      password: 'string1234'
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
