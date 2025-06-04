async function loadOrderPage() {
    const params = new URLSearchParams(window.location.search);
    const film = params.get("film");
    const time = params.get("time");
    const hall_id = params.get("hall_id");
    const date_id = params.get("date_id");
    const showing_id = params.get("showing_id");
    const date = params.get("date") || "Nieznana data";
    sessionStorage.setItem("order_url", window.location.href);
    const currentReservationKey = `selectedSeats_${showing_id}`;

    const storedSeats_ids = JSON.parse(sessionStorage.getItem(currentReservationKey)) || [];
    const storedSeats = JSON.parse(sessionStorage.getItem(currentReservationKey+"_seatNum")) || [];
    const summaryContainer = document.getElementById("summary");
    const totalDisplay = document.getElementById("total");

    const token = sessionStorage.getItem("access_token");
    const res = await fetch(`http://localhost:8000/reservations/prices`, {
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
    const prices_fetch = await res.json();



    const prices_grouped = {};
    prices_fetch.forEach(price => {
        prices_grouped[price.id] = [price.type, price.ticket_price];
    });
    const price_types = prices_fetch.map(price => price.type);

    const ticketPrices = {};
    prices_fetch.forEach(price => {
    ticketPrices[price.type] = price.ticket_price;
    });

    function updateTotal() {
        let total = 0;
        const selectors = summaryContainer.querySelectorAll("select");
        selectors.forEach(select => {
            total += ticketPrices[select.value];
        });
        totalDisplay.textContent = total;
        sessionStorage.setItem("total_payment", JSON.stringify(total)); // !!!!
    }

    if (storedSeats.length > 0) {
        storedSeats.forEach(seat => {
            const seatRow = document.createElement("div");
            seatRow.classList.add("seat-row");

            const seatLabel = document.createElement("span");
            seatLabel.textContent = `Miejsce ${seat}: `;

            const ticketSelect = document.createElement("select");
            price_types.forEach(type => {
                const option = document.createElement("option");
                option.value = type;
                option.textContent = `${type} (${ticketPrices[type]} zł)`;
                if (type === "normal") {
                    option.selected = true;
                }
                ticketSelect.appendChild(option);
            });

            ticketSelect.addEventListener("change", updateTotal);

            seatRow.appendChild(seatLabel);
            seatRow.appendChild(ticketSelect);
            summaryContainer.appendChild(seatRow);
        });

        updateTotal();
    } else {
        summaryContainer.textContent = "Nie wybrano żadnych miejsc.";
        totalDisplay.textContent = "0";
    }
    // powrót do odpowiedniej instancji reservation.html
    const returnBtn = document.getElementById("return-button");
    const returnUrl = sessionStorage.getItem("reservation_url") || "home.html";
    returnBtn.addEventListener("click", () => {
        window.location.href = returnUrl;
    });

    const transaction_id = 0
    const paymentBtn = document.getElementById("payment-button");
    const paymentUrl = `payment.html?showing_id=${encodeURIComponent(showing_id)}&transaction_id=${encodeURIComponent(transaction_id)}`;

    paymentBtn.addEventListener("click", async () => {
        const token = sessionStorage.getItem("access_token");
        try {
            const res = await fetch(`http://localhost:8000/reservations/reservations/${showing_id}`, {
                method: 'GET',
                headers: {
                'Authorization': `Bearer ${token}`
                }
            });

            if (res.status === 401) {
                alert("Unauthorized. Please log in again.");
                window.location.href = "login.html";
                return;
            }

            if (!res.ok) throw new Error("Błąd podczas sprawdzania dostępnych miejsc.");

            const takenSeats = await res.json();
            const takenSeatIds = Array.isArray(takenSeats)
            ? takenSeats.map(seat => seat.id?.toString()).filter(Boolean)
            : [];
            const selectedSeats = JSON.parse(sessionStorage.getItem(`selectedSeats_${showing_id}`)) || [];

            const conflictSeats = selectedSeats.filter(seat => takenSeatIds.includes(seat));

            if (conflictSeats.length > 0) {
                alert(`Niektóre z wybranych miejsc zostały już zarezerwowane: ${conflictSeats.join(", ")}.\nProszę wrócić i wybrać inne miejsca.`);
                window.location.href = sessionStorage.getItem("reservation_url");
            } else {
                window.location.href = paymentUrl;
            }

        } catch (error) {
            console.error("Błąd podczas sprawdzania dostępności miejsc:", error);
            alert("Wystąpił problem z weryfikacją miejsc. Spróbuj ponownie później.");
        }
});
}

window.addEventListener("load", loadOrderPage);