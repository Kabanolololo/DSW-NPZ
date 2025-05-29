import React, { useEffect, useState } from 'react'
import '../styles/profile.css'
import { getProfile } from '../api/auth' // upewnij się, że ta funkcja działa poprawnie

export default function ProfilePage() {
  const [email, setEmail] = useState('')

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getProfile()
        setEmail(data.email)
      } catch (err) {
        console.error('Błąd pobierania profilu:', err)
      }
    }

    fetchProfile()
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    window.location.href = '/login'
  }

  return (
    <div className="profile-container">
      <aside className="sidebar">
        {email && <p className="user-email">{email}</p>}
        <h2>Moje konto</h2>
        <ul>
          <li><a href="#">Galeria samochodów</a></li>
          <li><a href="/reservations">Moje rezerwacje</a></li>
          <li><a href="/cars">Utwórz rezerwację</a></li>
        </ul>
        <button className="logout-button" onClick={handleLogout}>Wyloguj się</button>
      </aside>

      <main className="main-content">
        <div className="gallery-grid">
          {/* 1. Kolumna */}
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

          {/* 2. Kolumna */}
          <div className="car-block">
            <div className="left-large">
              <img src="/svj.jpg" alt="Lamborghini Aventador SVJ" />
              <p className="caption">Lamborghini Aventador SVJ</p>
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
        </div>
      </main>
    </div>
  )
}
