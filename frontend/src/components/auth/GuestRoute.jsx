// Only unauthenticated users can access this route, e.g. login / sign up

import { useAuthContext } from '../../context/AuthContext.jsx';
import { Navigate} from 'react-router';

export default function GuestRoute({ children }) {
  const { isAuthenticated } = useAuthContext();

  if (isAuthenticated) {
    return <Navigate to="/settings" replace />  
  }

  return children;
}

