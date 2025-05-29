import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API_URL = 'http://localhost:8000' // lub IP backendu w razie potrzeby

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    email: '',
    address: '',
    city: '',
    password: '',
  })
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    try {
      const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Rejestracja nie powiodła się')
      }

      // Po rejestracji przenosimy na stronę logowania
      navigate('/login')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Rejestracja</h2>
      <form onSubmit={handleSubmit}>
        {error && <p style={{ color: 'red' }}>{error}</p>}

        <input name="name" placeholder="Imię" value={formData.name} onChange={handleChange} required />
        <br /><br />
        <input name="surname" placeholder="Nazwisko (opcjonalnie)" value={formData.surname} onChange={handleChange} />
        <br /><br />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <br /><br />
        <input name="address" placeholder="Adres" value={formData.address} onChange={handleChange} required />
        <br /><br />
        <input name="city" placeholder="Miasto" value={formData.city} onChange={handleChange} required />
        <br /><br />
        <input type="password" name="password" placeholder="Hasło" value={formData.password} onChange={handleChange} required />
        <br /><br />

        <button type="submit">Zarejestruj się</button>
      </form>
    </div>
  )
}
