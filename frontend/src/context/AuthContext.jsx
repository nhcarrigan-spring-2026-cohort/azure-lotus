import { createContext, useContext, useState } from 'react';
import { setAxiosAccessToken } from '../lib/axios.js';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState(null);

  const loginSuccess = (payload) => {
    const token = payload.user_info.access_token;
    setIsAuthenticated(true);
    setAccessToken(token);
    setAxiosAccessToken(token);
    setUser(payload.user_info);
  };

  const logout = () => {
    // TODO: use backend logout endpoint
    setIsAuthenticated(false);
    setAccessToken(null);
    setAxiosAccessToken(null);
    setUser(null);
  };

  const authValue = {
    loginSuccess,
    logout,
    user,
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
