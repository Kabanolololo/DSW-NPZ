import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getCarById } from '../api/auth'; // stworzymy za chwilę
import { useNavigate } from 'react-router-dom';

export default function CarDetailsPage() {
  const { id } = useParams();
  const [car, setCar] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    getCarById(id, token)
      .then(data => setCar(data))
      .catch(err => {
        setError(err.message);
      });
  }, [id, navigate]);

  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!car) return <p>Ładowanie...</p>;

  return (
    <div style={{ padding: '2rem' }}>
      <h2>{car.make} {car.model}</h2>
      <p><strong>Rok:</strong> {car.year}</p>
      <p><strong>Cena za dzień:</strong> {car.price_per_day} zł</p>
      <p><strong>Opis:</strong> {car.description}</p>
      <button onClick={() => navigate(`/reservations/create?car_id=${car.id}`)}>
        Zarezerwuj ten samochód
      </button>
    </div>
  );
}
