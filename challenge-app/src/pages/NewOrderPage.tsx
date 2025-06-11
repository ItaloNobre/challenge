import OrderForm from '../components/OrderForm';
import { Link } from 'react-router-dom';

export default function NewOrderPage() {
  return (
    <div className="container p-4">
      <Link to="/orders" className="btn btn-link mb-3">&larr; Voltar</Link>
      <OrderForm />
    </div>
  );
}
