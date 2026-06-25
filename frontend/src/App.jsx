import { Route, Routes } from 'react-router';
import Navbar from './components/Navbar.jsx';
import About from './pages/about.jsx';
import Home from './pages/Home.jsx';
import Login from './pages/Login.jsx';
import Signup from './pages/Signup.jsx';
import NotFound from './pages/NotFound.jsx';
import InviteVolunteers from './pages/InviteVolunteers.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Settings from './pages/Settings.jsx';
import Footer from './components/ui/Footer.jsx';
import HomeSenior from './pages/HomeVariations/HomeSenior/HomeSenior.jsx'
import ProtectedRoute from './components/auth/ProtectedRoute.jsx';
import GuestRoute from './components/auth/GuestRoute.jsx';
import { useLocation } from 'react-router';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './lib/query-client.js';
import { AuthProvider } from './context/AuthContext.jsx';

export default function App() {
    const location = useLocation();
    // map path to navbar type
  const getNavType = () => {
    const path = location.pathname;
    if (path === '/dashboard') return 'dashboard';
    if (path === '/checkin')   return 'checkin';
    if (path === '/settings')  return 'settings';
    return 'default';  // home, about,signup,login.
  };

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Navbar type={getNavType()} /> {/*Navbar rendered at top level with dynamic type */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          {/* <Route path="/explained" element={<Explained />} /> */}
          <Route
            path="/signup"
            element={
              <GuestRoute>
                <Signup />
              </GuestRoute>
            }
          />
          <Route
            path="/login"
            element={
              <GuestRoute>
                <Login />
              </GuestRoute>
            }
          />
          
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <Settings />
              </ProtectedRoute>
            }
          />
          <Route path="/checkin" element={
            <ProtectedRoute>
            <HomeSenior />
             </ProtectedRoute>
            } />
          <Route path="/invitevolunteers" element={<InviteVolunteers />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Footer />
      </AuthProvider>
    </QueryClientProvider>
  );
}
