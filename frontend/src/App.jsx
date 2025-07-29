import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './store/AuthContext';
import { AppProvider } from './store/AppContext';
import PrivateRoute from './components/auth/PrivateRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import History from './pages/History';
import Layout from './components/common/Layout';

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppProvider>
          <Routes>
            {/* Rotas públicas */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Rotas privadas */}
            <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="profile" element={<Profile />} />
              <Route path="history" element={<History />} />
            </Route>
            
            {/* Rota 404 */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </AppProvider>
      </AuthProvider>
    </Router>
  );
}

export default App
