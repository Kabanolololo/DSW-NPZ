import { useEffect, useState } from "react";
import { getReservationsByUser, deleteReservation, getCurrentUser } from "../api/auth";
import "../styles/myReservations.css";
import { useNavigate } from "react-router-dom";

export default function MyReservationsPage() {
  const [reservations, setReservations] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [userId, setUserId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchReservations = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setError("Nie jesteś zalogowany.");
        setLoading(false);
        return;
      }

      try {
        const user = await getCurrentUser(token); // 🔥 pobierz user ID
        setUserId(user.id);

        const res = await getReservationsByUser(token);
        setReservations(res);
      } catch (err) {
        setError("Nie udało się pobrać rezerwacji.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchReservations();
  }, []);

  const handleDelete = async (id) => {
    const token = localStorage.getItem("token");
    try {
      await deleteReservation(id, userId, token);
      setReservations((prev) => prev.filter((res) => res.id !== id));
    } catch (err) {
      alert("Nie udało się usunąć rezerwacji.");
      console.error(err);
    }
  };

  return (
    <div className="reservations-container">
      <button
        onClick={() => navigate("/profile")}
        className="back-button"
      >
        ← Powrót do profilu
      </button>

      <h2>Moje rezerwacje</h2>

      {loading && <p>Ładowanie rezerwacji...</p>}
      {error && <p className="error-text">{error}</p>}
      {!loading && !reservations.length && !error && (
        <p>Brak rezerwacji.</p>
      )}

      <ul className="reservation-list">
        {reservations.map((res) => (
          <li key={res.id} className="reservation-item">
            <strong>
              {res.car?.brand} {res.car?.model}
            </strong><br />
            Od: <span>{res.start_date?.slice(0, 10)}</span><br />
            Do: <span>{res.end_date?.slice(0, 10)}</span><br />
            Cena: <span>{res.car?.price_per_day} PLN/dzień</span><br />
            <button className="delete-button" onClick={() => handleDelete(res.id)}>Usuń</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
