import { Routes, Route } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProfilePage from './pages/ProfilePage'
import CarsPage from './pages/CarsPage'
import CarDetailsPage from './pages/CarDetailsPage'
import AddCarPage from './pages/AddCarPage'
import CreateReservationPage from './pages/CreateReservationPage'
import ReserveCarPage from './pages/ReserveCarPage'
import MyReservationsPage from './pages/MyReservationsPage'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/profile" element={<ProfilePage />} />
      <Route path="/cars" element={<CarsPage />} />
      <Route path="/cars/:id" element={<CarDetailsPage />} />
      <Route path="/add-car" element={<AddCarPage />} />
      <Route path="/reservation/create" element={<CreateReservationPage />} />
      <Route path="/reservation/:carId" element={<ReserveCarPage />} />
      <Route path="/reservations" element={<MyReservationsPage />} />
      
    </Routes>
  )
}

export default App
