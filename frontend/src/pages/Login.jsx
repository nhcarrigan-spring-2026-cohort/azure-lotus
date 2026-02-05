import { useAuthContext } from '../context/AuthContext.jsx';

const Login = () => {
  const { login } = useAuthContext();

  const handleLogin = async (e) => {
    e.preventDefault();
    await login.mutateAsync({ username: 'emilys', password: 'emilyspass' });
  };

  return (
    <button onClick={handleLogin} disabled={login.isPending}>
      Login
    </button>
  );
};

export default Login;
