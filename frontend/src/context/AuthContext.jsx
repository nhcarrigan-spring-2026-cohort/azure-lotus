import { createContext, useContext, useState } from 'react';
import api from '../lib/axios.js';
import { useMutation } from '@tanstack/react-query';
import {useNavigate} from 'react-router'

const AuthContext = createContext(null);

/* Requests */
const loginRequest = async ({ email, password }) => {
  const { data } = await api.post('/auth/login', {
    email,
    password,
  });
  return data;
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  let navigate = useNavigate()

  const login = useMutation({
    mutationFn: loginRequest,
    onSuccess: (user) => {
      console.log(`Login successful, ${JSON.stringify(user)}`);
      setIsAuthenticated(true);
      setUser(user.user_info);
      navigate('/')
    },
  });

  const logout = () => {
    // TODO: use backend logout endpoint
    setIsAuthenticated(false);
  };

  const authValue = {
    login,
    logout,
    user,
    isAuthenticated,
  };

  return (
    <AuthContext.Provider value={authValue}>{children}</AuthContext.Provider>
  );
}

export const useAuthContext = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
};
