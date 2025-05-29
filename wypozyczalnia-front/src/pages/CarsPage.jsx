import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/cars.css';

export default function CarsPage() {
  const [cars, setCars] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    fetch('http://localhost:8000/cars', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => {
        if (!res.ok) {
          throw new Error('Błąd podczas pobierania samochodów');
        }
        return res.json();
      })
      .then(data => setCars(data))
      .catch(err => {
        setError(err.message);
        navigate('/login');
      });
  }, [navigate]);

  if (error) {
    return <p style={{ color: 'red' }}>{error}</p>;
  }

  if (!cars.length) {
    return <p>Ładowanie samochodów...</p>;
  }

  return (
    <div className="cars-container">
      <button onClick={() => navigate('/profile')} className="back-button">
        ← Powrót do profilu
      </button>

      <h2 className="cars-title">Dostępne samochody</h2>

      <div className="cars-grid">
        {cars.map(car => (
          <div className="car-card" key={car.id}>
            <img
              className="car-image"
              src={`/cars/${car.model.toLowerCase()}.jpg`}
              alt={`${car.brand} ${car.model}`}
            />
            <div className="car-details">
              <h3>{car.brand} {car.model}</h3>
              <p>Rok produkcji: {car.year}</p>
              <p>Cena za dzień: {car.price_per_day} PLN</p>
              <button onClick={() => navigate(`/reservation/${car.id}`)}>
                Zarezerwuj
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
