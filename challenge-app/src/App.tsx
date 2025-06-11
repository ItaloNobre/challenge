import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import OrdersPage from './pages/OrdersPage';
import NewOrderPage from './pages/NewOrderPage';
import type { JSX } from 'react';

function Protected({ children }: { children: JSX.Element }) {
  return localStorage.getItem('token') ? children : <Navigate to="/" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/orders" element={
          <Protected><OrdersPage /></Protected>
        } />
        <Route path="/orders/new" element={
          <Protected><NewOrderPage /></Protected>
        } />
      </Routes>
    </BrowserRouter>
  );
}
