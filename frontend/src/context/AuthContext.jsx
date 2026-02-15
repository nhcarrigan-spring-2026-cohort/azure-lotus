import { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [accessToken, setAccessToken] = useState(null);

  const loginSuccess = (payload) => {
    setIsAuthenticated(true);
    setAccessToken(payload.access_token);
    setUser(payload.user_info);
  };

  const logout = () => {
    // TODO: use backend logout endpoint
    setIsAuthenticated(false);
    setAccessToken(null);
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
