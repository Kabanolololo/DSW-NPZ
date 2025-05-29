import React, { useEffect, useState } from 'react';
import '../styles/profile.css';
import { getProfile } from '../api/auth';
import { useNavigate } from 'react-router-dom';

export default function ProfilePage() {
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getProfile();
        setEmail(data.email);
      } catch (err) {
        console.error('Błąd pobierania profilu:', err);
      }
    };

    fetchProfile();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    <div className="profile-container">
      <aside className="sidebar">
        <p className="user-email">{email}</p>
        <h2>Moje konto</h2>

        <div className="sidebar-links">
          <button className="sidebar-button" onClick={() => navigate('')}>
            Galeria samochodów
          </button>
          <button className="sidebar-button" onClick={() => navigate('/reservations')}>
            Moje rezerwacje
          </button>
          <button className="sidebar-button" onClick={() => navigate('/cars')}>
            Utwórz rezerwację
          </button>
        </div>

        <div className="sidebar-bottom">
          <button
            className="add-car-button"
            onClick={() => navigate('/add-car')}
          >
            +
          </button>

          <button className="logout-button" onClick={handleLogout}>
            Wyloguj się
          </button>
        </div>
      </aside>

      <main className="main-content">
        <div className="gallery-grid">
          {/* Kolumna 1 */}
          <div className="car-block">
            <div className="left-large">
              <img src="/aventador.jpg" alt="Lamborghini Aventador" />
              <p className="caption">Lamborghini Aventador</p>
            </div>
            <div className="right-small">
              <div>
                <img src="/porshe.jpg" alt="Porsche 911" />
                <p className="caption">Porsche 911</p>
              </div>
              <div>
                <img src="/bentley.jpg" alt="Bentley Continental GT" />
                <p className="caption">Bentley Continental GT</p>
              </div>
            </div>
          </div>

          {/* Kolumna 2 */}
          <div className="car-block">
            <div className="left-large">
              <img src="/ferrari.jpg" alt="Ferarri" />
              <p className="caption">Ferrari Enzo</p>
            </div>
            <div className="right-small">
              <div>
                <img src="/gtramg.jpg" alt="gtr amg" />
                <p className="caption">Mercedes AMG GT-R</p>
              </div>
              <div>
                <img src="/gtrblue.jpg" alt="gtrblue" />
                <p className="caption">Nissan GTR LBWK</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
