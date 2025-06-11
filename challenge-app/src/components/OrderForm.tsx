import { useState } from 'react';
import api from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function OrderForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handle = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post('/order/create/', { title, description });
      navigate('/orders');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handle}>
      <h3 className="mb-4">Novo Pedido</h3>

      <input
        className="form-control mb-3"
        placeholder="Título do pedido"
        value={title}
        onChange={e => setTitle(e.target.value)}
        required
        disabled={loading}
      />

      <textarea
        className="form-control mb-3"
        placeholder="Descrição do pedido"
        value={description}
        onChange={e => setDescription(e.target.value)}
        required
        disabled={loading}
        rows={3}
      />

      <button className="btn btn-success" disabled={loading}>
        {loading ? 'Enviando...' : 'Solicitar'}
      </button>
    </form>
  );
}
