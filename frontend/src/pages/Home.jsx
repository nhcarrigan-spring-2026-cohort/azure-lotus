import useTitle from '../components/hooks/useTitle';

/* import { Link } from 'react-router';
import { useState } from 'react';
import { Route, Routes } from 'react-router'; */  /* TODO: Delete later  */
import Dashboard from './Dashboard.jsx';
/* import CheckIn from '../components/checkin/CheckIn'; */
import './Home.css';
import { useAuthContext } from '../context/AuthContext.jsx';
import ProtectedRoute from '../components/auth/ProtectedRoute.jsx';


export default function Home() {
  useTitle();
  const { user, isAuthenticated } = useAuthContext();
  

  return (
    <>
      {isAuthenticated ? (     //here we should check if the user is a senior or a family member, the home differs
        <>
          {/* <CheckIn /> */}
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        </>
      ) : (
        <a href="/login">Login</a>
      )}
    </>
  );
}
