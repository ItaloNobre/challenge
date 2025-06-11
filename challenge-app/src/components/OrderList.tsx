import { useEffect, useState } from 'react';
import api from '../api/client';
import { type Order } from '../types';

export default function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchOrders = () => {
    api.get('api/v1/pedidos/')
      .then(res => setOrders(res.data.results))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchOrders(); // primeira chamada

    const interval = setInterval(() => {
      fetchOrders(); // chamadas a cada 5 segundos
    }, 5000);

    return () => clearInterval(interval); // limpeza no unmount
  }, []);

  if (loading) return <p>Carregando pedidos...</p>;
  if (!orders.length) return <p>Nenhum pedido encontrado.</p>;

  return (
    <div className="container mt-4">
      <h3 className="mb-3">Lista de Pedidos</h3>
      <ul className="list-group">
        {orders.map(order => (
          <li
            key={order.id}
            className="list-group-item d-flex justify-content-between align-items-start"
          >
            <div>
              <strong>{order.title}</strong><br />
              <small className="text-muted">Status: {order.status.name}</small><br />
              <span>Descrição: {order.description}</span>
            </div>
            <span className="badge bg-secondary mt-1">Código: {order.code}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
