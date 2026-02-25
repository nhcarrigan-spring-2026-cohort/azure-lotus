import { Route, Routes } from 'react-router';
import Navbar from './components/Navbar.jsx';
import About from './pages/about.jsx';
import Explained from './pages/explained.jsx';
import Home from './pages/Home.jsx';
import Login from './pages/Login.jsx';
import Signup from './pages/Signup.jsx';
import NotFound from './pages/NotFound.jsx';
import InviteVolunteers from './pages/InviteVolunteers.jsx';
import Dashboard from './pages/Dashboard.jsx';
import CreateSenior from './pages/CreateSenior.jsx';

import ProtectedRoute from './components/auth/ProtectedRoute.jsx';
import GuestRoute from './components/auth/GuestRoute.jsx';

import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from './lib/query-client.js';
import { AuthProvider } from './context/AuthContext.jsx';

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/explained" element={<Explained />} />
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
          <Route path="/invitevolunteers" element={<InviteVolunteers />} />
          <Route path="/seniorprofilesetup" element={<CreateSenior />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthProvider>
    </QueryClientProvider>
  );
}
