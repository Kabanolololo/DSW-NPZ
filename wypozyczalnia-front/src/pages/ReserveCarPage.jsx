import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { makeReservation, getCurrentUser } from "../api/auth";

export default function ReserveCarPage() {
  const { carId } = useParams(); // carId pochodzi z URL-a: /reservation/:carId
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleReserve = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    if (!token) {
      setError("Musisz być zalogowany, aby dokonać rezerwacji.");
      return;
    }

    try {
      const user = await getCurrentUser(token);

      const reservationData = {
        user_id: user.id,
        car_id: parseInt(carId),
        start_date: `${startDate}T00:00:00`,
        end_date: `${endDate}T00:00:00`,
      };

      await makeReservation(reservationData, token, user.id);
      navigate('/reservations');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Zarezerwuj samochód</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleReserve}>
        <div>
          <label>Data rozpoczęcia:</label><br />
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
          />
        </div>

        <div style={{ marginTop: '1rem' }}>
          <label>Data zakończenia:</label><br />
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            required
          />
        </div>

        <button type="submit" style={{ marginTop: '1.5rem' }}>
          Zarezerwuj
        </button>
      </form>
    </div>
  );
}
