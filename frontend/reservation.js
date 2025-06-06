async function loadReservationPage() {
  const params = new URLSearchParams(window.location.search);
  const film = params.get("film");
  const time = params.get("time");
  const hall_id = params.get("hall_id");
  const date_id = params.get("date_id");
  const showing_id = params.get("showing_id");
  const date = params.get("date") || "Nieznana data";
  const headerDate = document.querySelector(".date");

  sessionStorage.setItem("reservation_url", window.location.href);
  
  const token = sessionStorage.getItem("access_token");
  const res = await fetch(`http://localhost:8000/reservations/reservations/${showing_id}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
  }
  });
  if (res.status === 401) {
    alert("Unauthorized. Please log in again.");
    window.location.href = "login.html";
  }
  if (!res.ok) throw new Error(`Błąd przy pobieraniu stanu miejsc z bazy`);
  const seats_fetch = await res.json();

  createSeatLayout(seats_fetch);

  if (film && headerDate) {
      headerDate.textContent = `Rezerwacja miejsc na seans: ${film} | ${date}, godz. ${time}`;
  }

  const seats = document.querySelectorAll(".seat:not(.occupied)");
  // zapisywane lokalnie miejsca - zachowane tylko dla ostatniego url showingu
  const currentReservationKey = `selectedSeats_${showing_id}`;
  const lastReservationId = sessionStorage.getItem("last_reservation_id");
  if (lastReservationId && lastReservationId !== showing_id) {
    Object.keys(sessionStorage).forEach(key => {
      if (key.startsWith("selectedSeats_") && key !== currentReservationKey) {
          sessionStorage.removeItem(key);
      }
  });
  }
  sessionStorage.setItem("last_reservation_id", showing_id);


  seats.forEach(seat => {
      seat.addEventListener("click", () => {
      seat.classList.toggle("selected");
      updateSelectionInfo(currentReservationKey);
      });
  });


  const savedSeats = JSON.parse(sessionStorage.getItem(currentReservationKey));
  if (savedSeats && Array.isArray(savedSeats)) {
      savedSeats.forEach(seatId => {
      const seat = document.getElementById(seatId);
      if (seat && !seat.classList.contains("occupied")) {
          seat.classList.add("selected");
      }
      });
      updateSelectionInfo(currentReservationKey);
  }

  const dalejBtn = document.getElementById("dalejBtn");
  dalejBtn.addEventListener("click", (e) => {
      const selectedSeats = JSON.parse(sessionStorage.getItem(currentReservationKey)) || [];

      if (selectedSeats.length === 0) {
      e.preventDefault();
      alert("Wybierz przynajmniej jedno miejsce, aby przejść dalej.");
      } else {
      const url = `order.html?film=${encodeURIComponent(film)}&time=${encodeURIComponent(time)}&date=${encodeURIComponent(date)}&date_id=${encodeURIComponent(date_id)}&hall_id=${encodeURIComponent(hall_id)}&showing_id=${encodeURIComponent(showing_id)}`;
      window.location.href = url;
      }
  });
}

function updateSelectionInfo(currentReservationKey) {
  const selectedSeats = document.querySelectorAll(".seat.selected");
  const seatIds = Array.from(selectedSeats).map(seat => seat.id);
  const seatNums = Array.from(selectedSeats).map(seat => seat.getAttribute("data-seat-num"));

  sessionStorage.setItem(currentReservationKey, JSON.stringify(seatIds));
  sessionStorage.setItem(currentReservationKey+"_seatNum", JSON.stringify(seatNums));
  document.querySelector("#selected-seats").textContent = seatNums.length > 0 
      ? `Wybrane miejsca: ${seatNums.join(", ")}`
      : "Brak wybranych miejsc.";
}

function createSeatLayout(seatsData) {
  const container = document.getElementById("seats-container");

  const rowsMap = new Map();
  seatsData.forEach(seat => {
    if (!rowsMap.has(seat.row)) {
      rowsMap.set(seat.row, []);
    }
    rowsMap.get(seat.row).push(seat);
  });

  rowsMap.forEach((rowSeats, rowIndex) => {
    rowSeats.sort((a, b) => a.seat_num - b.seat_num);

    const rowDiv = document.createElement("div");
    rowDiv.className = "row";
    rowDiv.id = `row-${rowIndex}`;

    const label = document.createElement("span");
    label.className = "row-label";
    label.textContent = rowIndex;
    rowDiv.appendChild(label);

    rowSeats.forEach(seat => {
      const btn = document.createElement("button");
      btn.className = "seat";
      if (seat.is_taken) btn.classList.add("occupied");
      btn.id = seat.seat_id;
      btn.textContent = seat.seat_num;
      btn.setAttribute("data-seat-num", seat.seat_num);
      rowDiv.appendChild(btn);
    });

    container.appendChild(rowDiv);
  });
}

window.addEventListener("load", loadReservationPage);