import { NavLink } from 'react-router-dom'
import '../styles/Sidebar.css'

export default function Sidebar() {
  return (
    <nav className="sidebar">
      <h2>Moje konto</h2>
      <ul>
        <li><NavLink to="reservations">Moje rezerwacje</NavLink></li>
        <li><NavLink to="/cars">Utwórz rezerwację</NavLink></li>
      </ul>
    </nav>
  )
}
