import { useEffect, useState } from 'react';
import { getInstallments, getPayments } from './api';

function App() {
  const [installments, setInstallments] = useState([]);
  const [payments, setPayments] = useState([]);

  useEffect(() => {
    getInstallments().then(res => setInstallments(res.data));
    getPayments().then(res => setPayments(res.data));
  }, []);

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Installments</h1>
      <ul>
        {installments.map(i => (
          <li key={i.id}>{JSON.stringify(i)}</li>
        ))}
      </ul>

      <h1>Payments</h1>
      <ul>
        {payments.map(p => (
          <li key={p.id}>{JSON.stringify(p)}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;