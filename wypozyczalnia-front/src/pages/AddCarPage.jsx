import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createCar} from '../api/auth';

export default function AddCarPage() {
  const [form, setForm] = useState({
    brand: '',
    model: '',
    year: '',
    color: '',
    price_per_day: '',
    availability: 'available'
  });

  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  const token = localStorage.getItem('token');
  if (!token) {
    setError('Musisz być zalogowany, aby dodać samochód.');
    return;
  }

  try {
    await createCar(form, token); // ← najważniejsza zmiana
    navigate('/cars');
  } catch (err) {
    setError(err.message);
  }
};


  return (
    <div style={{ padding: '2rem' }}>
      <h2>Dodaj nowy samochód</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input name="brand" placeholder="Marka" value={form.brand} onChange={handleChange} required /><br />
        <input name="model" placeholder="Model" value={form.model} onChange={handleChange} required /><br />
        <input name="year" placeholder="Rok produkcji" type="number" value={form.year} onChange={handleChange} required /><br />
        <input name="color" placeholder="Kolor" value={form.color} onChange={handleChange} required /><br />
        <input name="price_per_day" placeholder="Cena za dzień" type="number" value={form.price_per_day} onChange={handleChange} required /><br />
        <select name="availability" value={form.availability} onChange={handleChange}>
          <option value="available">Dostępny</option>
          <option value="unavailable">Niedostępny</option>
        </select><br /><br />

        <button type="submit">Dodaj samochód</button>
      </form>
    </div>
  );
}
