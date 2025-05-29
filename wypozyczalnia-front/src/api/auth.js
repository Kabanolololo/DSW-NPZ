const API_URL = 'http://localhost:8000';

// ✅ Logowanie użytkownika
export async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    throw new Error('Niepoprawne dane logowania');
  }

  const data = await response.json();
  return data;
}

// ✅ Pobieranie danych zalogowanego użytkownika (token w query!)
export async function getCurrentUser(token) {
  const response = await fetch(`${API_URL}/auth/me?token=${token}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error('Nie udało się pobrać danych użytkownika');
  }

  return await response.json();
}

// ✅ Pobieranie danych konkretnego auta
export async function getCarById(id, token) {
  const response = await fetch(`${API_URL}/cars/${id}`, {
    headers: {
      'Content-Type': 'application/json',
      // Można dodać token, jeśli backend go wymaga (w query lub w nagłówku)
      Authorization: `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error('Nie udało się pobrać danych auta');
  }

  return await response.json();
}




// ✅ Dodawanie auta jako admin (token w query!)
export async function createCar(carData, token) {
  const response = await fetch(`${API_URL}/cars/admin?token=${token}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(carData),
  });

  if (!response.ok) {
    throw new Error('Nie udało się dodać samochodu');
  }

  return await response.json();
}

export async function getProfile() {
  const token = localStorage.getItem('token')

  const res = await fetch('http://localhost:5000/auth/me?token=' + token)
  if (!res.ok) throw new Error('Nie udało się pobrać profilu')

  return res.json()
}

export async function makeReservation(data, token, userId) {
  const response = await fetch(`http://localhost:8000/reservations/?user_id=${userId}&token=${token}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Nie udało się zarezerwować samochodu");
  }

  return response.json();
}

export async function getReservationsByUser(token) {
  const res = await fetch(`http://localhost:8000/reservations/me?token=${token}`);
  if (!res.ok) {
    throw new Error("Nie udało się pobrać rezerwacji użytkownika");
  }
  return res.json();
}


export async function deleteReservation(id, userId, token) {
  const res = await fetch(`http://localhost:8000/reservations/${id}?user_id=${userId}&token=${token}`, {
    method: 'DELETE',
  });

  if (!res.ok) {
    throw new Error('Nie udało się usunąć rezerwacji');
  }

  return await res.json();
}

