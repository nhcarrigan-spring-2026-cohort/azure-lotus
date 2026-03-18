import { createContext, useContext, useState } from 'react';
import { setAxiosAccessToken } from '../lib/axios.js';
import api from '../lib/axios.js';

const AuthContext = createContext(null);
import { useEffect } from 'react';

export function AuthProvider({ children }) {
  useEffect(() => {
    refreshToken();
  }, []);

  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // TODO: we can probably remove accessToken here and let the axios instance and
  // interceptors handle it
  const [accessToken, setAccessToken] = useState(null);
  const [isAuthReady, setIsAuthReady] = useState(false)

  const loginSuccess = (payload,navigate) => {
    const token = payload.user_info.access_token;
    setIsAuthenticated(true);
    setAccessToken(token);
    setAxiosAccessToken(token);
    setUser(payload.user_info);
    setIsAuthReady(true)
    navigate('/settings', { replace: true });
  };

  const logout = () => {
    // TODO: use backend logout endpoint
    setIsAuthenticated(false);
    setAccessToken(null);
    setAxiosAccessToken(null);
    setUser(null);
    setIsAuthReady(true)
  };

  const refreshToken = async () => {
    try {
      const res = await api.post('/auth/refresh');
      setAccessToken(res.data.access_token);
      setUser(res.data.user_info);
      setIsAuthenticated(true);
    } catch (error) {
      setAccessToken(null);
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setIsAuthReady(true)
    }
  };

  const authValue = {
    loginSuccess,
    logout,
    user,
    isAuthenticated,
    accessToken,
    isAuthReady
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
