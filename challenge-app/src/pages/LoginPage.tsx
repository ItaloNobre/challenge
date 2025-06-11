import LoginForm from '../components/LoginForm';

export default function LoginPage() {
  return (
    <div className="container d-flex justify-content-center align-items-center" style={{height:'100vh'}}>
      <div className="card p-4" style={{minWidth: '350px'}}>
        <LoginForm />
      </div>
    </div>
  );
}
