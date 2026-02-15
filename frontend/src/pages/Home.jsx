import useTitle from '../components/hooks/useTitle';
import './Home.css';
import { useAuthContext } from '../context/AuthContext.jsx';

export default function Home() {
  const { user, isAuthenticated } = useAuthContext();
  useTitle();

  return (
    <>
      <h1>Home</h1>
      {isAuthenticated ? (
        <p>Welcome, {user?.email}!</p>
      ) : (
        <a href="/login">Login</a>
      )}
    </>
  );
}
