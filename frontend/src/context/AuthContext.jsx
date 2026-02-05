import { createContext, useContext, useState } from 'react';
import api from '../lib/axios.js';
import { useMutation } from '@tanstack/react-query';

const AuthContext = createContext(null);

/* Requests */
const loginRequest = async ({ username, password }) => {
  const { data } = await api.post('/auth/login', {
    username,
    password,
  });
  return data;
};

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = useMutation({
    mutationFn: loginRequest,
    onSuccess: (user) => {
      console.log(`Login successful, ${JSON.stringify(user)}`);
      setAccessToken(user.accessToken);
      setIsAuthenticated(true);
    },
  });

  const authValue = {
    login,
    isAuthenticated,
    accessToken,
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
