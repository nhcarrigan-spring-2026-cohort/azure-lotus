// Only unauthenticated users can access this route, e.g. login / sign up

import { useAuthContext } from '../../context/AuthContext.jsx';
import { Navigate, useLocation } from 'react-router';

export default function GuestRoute({ children }) {
  const { isAuthenticated } = useAuthContext();
  const location = useLocation();

  if (isAuthenticated) {
    return <Navigate to="/settings" replace />  // ← directly redirect
  }

  return children;
}

