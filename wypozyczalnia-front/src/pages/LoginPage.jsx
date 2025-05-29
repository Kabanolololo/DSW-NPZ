import { useState } from 'react'
import { loginUser } from '../api/auth'
import { useNavigate, Link } from 'react-router-dom'
import '../styles/LoginPage.css' // styl dołączony osobno

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const data = await loginUser(email, password)
      localStorage.setItem('token', data.access_token)
      navigate('/profile') // przekierowanie po zalogowaniu
    } catch (err) {
      setError('Nieprawidłowy email lub hasło.')
    }
  }

  return (
    <div className="login-background">
      <div className="login-container">
        <form className="login-box" onSubmit={handleSubmit}>
          <h2 className="login-title">Luxury Car Rental</h2>

          {error && <p className="error-text">{error}</p>}

          <label>Email:</label>
          <input
            type="email"
            placeholder="kuba2003@gmail.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Hasło:</label>
          <input
            type="password"
            placeholder="********"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button type="submit">Zaloguj się</button>

          <div className="register-link">
            <a href="/register">Zarejestruj się</a>
          </div>

        </form>
      </div>
    </div>
  )
}
