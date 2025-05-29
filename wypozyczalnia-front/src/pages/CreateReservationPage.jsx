import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { makeReservation } from '../api/auth';
import { getCurrentUser } from '../api/auth';

export default function CreateReservationPage() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [userId, setUserId] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  // Wyciągamy car_id z query params
  const params = new URLSearchParams(location.search);
  const carId = params.get('car_id');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    getCurrentUser(token)
      .then(user => setUserId(user.id))
      .catch(() => {
        localStorage.removeItem('token');
        navigate('/login');
      });
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      await makeReservation({ user_id: userId, car_id: parseInt(carId), start_date: startDate, end_date: endDate }, token);
      navigate('/reservations'); // <- przekierowanie po sukcesie
    } catch (err) {
      setError('Nie udało się złożyć rezerwacji.');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Zarezerwuj samochód</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Data początkowa:</label><br />
          <input type="datetime-local" value={startDate} onChange={e => setStartDate(e.target.value)} required />
        </div>
        <div style={{ marginTop: '1rem' }}>
          <label>Data końcowa:</label><br />
          <input type="datetime-local" value={endDate} onChange={e => setEndDate(e.target.value)} required />
        </div>
        <button type="submit" style={{ marginTop: '1rem' }}>Zarezerwuj</button>
      </form>
    </div>
  );
}
