import { createContext, useContext, useState } from 'react';
// import api from '../lib/axios.js';
// import {useMutation} from '@tanstack/react-query';
// import {useNavigate} from 'react-router'

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

  // let navigate = useNavigate()

  // const register = useMutation({
  //     mutationFn: registerRequest,
  //     onSuccess: (user) => {
  //         console.log(`Registration successful, ${JSON.stringify(user)}`);
  //     },
  //     onError: (error) => {
  //         // TODO: frontend should show user the error
  //         console.log(`Registration failed, ${JSON.stringify(error.message)}`);
  //     }
  // })

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
