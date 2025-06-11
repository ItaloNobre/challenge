import { useNavigate, Link } from 'react-router-dom';
import OrderList from '../components/OrderList';

export default function OrdersPage() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate(-1);
  };

  return (
    <div className="container p-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        {/* Botão Deslogar arredondado (pill) */}
        <button
          onClick={handleLogout}
          className="btn btn-danger rounded-pill"
          style={{ minWidth: '100px' }}
          title="Deslogar"
        >
          Deslogar
        </button>

        {/* Botão + Novo arredondado (pill) */}
        <Link
          to="/orders/new"
          className="btn btn-primary rounded-pill"
          style={{ minWidth: '100px' }}
          title="Novo Pedido"
        >
          + Novo
        </Link>
      </div>

      <OrderList />
    </div>
  );
}
