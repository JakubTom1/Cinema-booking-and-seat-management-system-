async function loadReservationPage() {
    const params = new URLSearchParams(window.location.search);
    const film = params.get("film");
    const time = params.get("time");
    const hall_id = params.get("hall_id");
    const date_id = params.get("date_id");
    const showing_id = params.get("showing_id");
    const date = params.get("date") || "Nieznana data";
    const headerDate = document.querySelector(".date");

    const res = await fetch(`http://localhost:8000/reservations/reservations/${showing_id}`);
    const seats_fetch = await res.json();

    createSeatLayout(seats_fetch);

    if (film && headerDate) {
        headerDate.textContent = `Rezerwacja miejsc na seans: ${film} | ${date}, godz. ${time}`;
    }

    const seats = document.querySelectorAll(".seat:not(.occupied)");

    seats.forEach(seat => {
        seat.addEventListener("click", () => {
        seat.classList.toggle("selected");
        updateSelectionInfo();
        });
    });

    const savedSeats = JSON.parse(sessionStorage.getItem("selectedSeats"));
    if (savedSeats && Array.isArray(savedSeats)) {
        savedSeats.forEach(seatId => {
        const seat = document.getElementById(seatId);
        if (seat && !seat.classList.contains("occupied")) {
            seat.classList.add("selected");
        }
        });
        updateSelectionInfo();
    }

    const dalejBtn = document.getElementById("dalejBtn");
    dalejBtn.addEventListener("click", (e) => {
        const selectedSeats = JSON.parse(sessionStorage.getItem("selectedSeats")) || [];

        if (selectedSeats.length === 0) {
        e.preventDefault();
        alert("Wybierz przynajmniej jedno miejsce, aby przejść dalej.");
        } else {
        window.location.href = "order.html";
        }
    });
}

function updateSelectionInfo() {
    const selectedSeats = document.querySelectorAll(".seat.selected");
    const seatIds = Array.from(selectedSeats).map(seat => seat.id);

    sessionStorage.setItem("selectedSeats", JSON.stringify(seatIds));

    document.querySelector("#selected-seats").textContent = seatIds.length > 0 
        ? `Wybrane miejsca: ${seatIds.join(", ")}`
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
      rowDiv.id = `row-${rowLabel(rowIndex)}`;

      const label = document.createElement("span");
      label.className = "row-label";
      label.textContent = rowLabel(rowIndex);
      rowDiv.appendChild(label);

      rowSeats.forEach(seat => {
        const btn = document.createElement("button");
        btn.className = "seat";
        if (seat.is_taken) btn.classList.add("occupied");
        btn.id = seat.seat_id;
        btn.textContent = seat.seat_num;
        rowDiv.appendChild(btn);
      });

      container.appendChild(rowDiv);
    });
  }

window.onload = loadReservationPage;