async function loadOrderPage() {
    const params = new URLSearchParams(window.location.search);
    const film = params.get("film");
    const time = params.get("time");
    const hall_id = params.get("hall_id");
    const date_id = params.get("date_id");
    const showing_id = params.get("showing_id");
    const date = params.get("date") || "Nieznana data";
    sessionStorage.setItem("order_url", window.location.href);
    sessionStorage.setItem("lastPage", window.location.href);
    const currentReservationKey = `selectedSeats_${showing_id}`;
    const headerDate = document.querySelector(".date");
    const storedSeats_ids = JSON.parse(sessionStorage.getItem(currentReservationKey)) || [];
    const storedSeats = JSON.parse(sessionStorage.getItem(currentReservationKey+"_seatNum")) || [];
    const summaryContainer = document.getElementById("summary");
    const totalDisplay = document.getElementById("total");
    const didTicketsExist = false
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

    if (film && headerDate) {
      headerDate.textContent = `Rezerwacja miejsc na seans: ${film} | ${date}, godz. ${time}`;
    }

    const prices_grouped = {};
    prices_fetch.forEach(price => {
        prices_grouped[price.id] = [price.type, price.ticket_price];
    });
    const priceTypeToId = {};
    prices_fetch.forEach(price => {
        priceTypeToId[price.type] = price.id;
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
        storedSeats.forEach((seat, index) => {
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

            const seatId = storedSeats_ids[index];

            ticketSelect.addEventListener("change", () => {
                updatePriceMapping(seatId, ticketSelect.value.split(" (")[0]);
                updateTotal();
            });

            updatePriceMapping(seatId, ticketSelect.value.split(" (")[0]);

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

    const paymentBtn = document.getElementById("payment-button");
    const existingTransactionId = sessionStorage.getItem("transactionId");

    if (existingTransactionId) {
        try {
            const response_existing = await fetch(`http://localhost:8000/reservations/tickets/${existingTransactionId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response_existing.status === 401) {
                alert("Unauthorized. Please log in again.");
                window.location.href = "login.html";
            }
            if (!response_existing.ok) throw new Error("Błąd przy sprawdzaniu istniejących biletów.");

            const existingTicketsRaw = await response_existing.json();
            const existingTickets = normalizeTickets(existingTicketsRaw);

            const seatPriceMap = JSON.parse(sessionStorage.getItem("seatPriceMap")) || {};
            const localTickets = JSON.parse(sessionStorage.getItem("ticketsData")) || {};

            const areSame = areArraysEqualIgnoringId(existingTickets, localTickets);
            if (areSame) {
                existingTickets.forEach(ticket => {
                    const seatId = ticket.id_seats;
                    const type = Object.keys(priceTypeToId).find(key => priceTypeToId[key] === ticket.id_pricelist);
                    if (type) {
                        seatPriceMap[seatId] = type;
                    }
                });
                sessionStorage.setItem("seatPriceMap", JSON.stringify(seatPriceMap));

                const selectors = summaryContainer.querySelectorAll("select");
                selectors.forEach((select, index) => {
                    const seatId = storedSeats_ids[index];
                    const type = seatPriceMap[seatId];
                    if (type) {
                        select.value = type;
                    }
                });

                updateTotal();

                alert('Wykryto oczekującą płatność dla twojego zamówienia! Przekierowanie do płatności...')
                const paymentUrl = `payment.html?showing_id=${encodeURIComponent(showing_id)}&transaction_id=${encodeURIComponent(existingTransactionId)}`;
                window.location.href = paymentUrl;
                return;
            }

        } catch (error) {
            console.error("Błąd podczas weryfikacji istniejącej transakcji:", error);
            alert("Wystąpił problem przy weryfikacji zapisanych danych. Spróbuj ponownie.");
        }
    }


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
            const takenSeatIds = [];
            takenSeats.forEach(seat => {
                if (seat.is_taken === true && seat.seat_id !== null) {
                    takenSeatIds.push(seat.seat_id.toString())
                }
            })
            const selectedSeats = JSON.parse(sessionStorage.getItem(`selectedSeats_${showing_id}`)) || [];
            const conflictSeats = selectedSeats.filter(seat => takenSeatIds.includes(seat));
            if (conflictSeats.length > 0) {
                alert(`Niektóre z wybranych miejsc zostały już zarezerwowane. Proszę wrócić i wybrać inne miejsca.`);
                window.location.href = sessionStorage.getItem("reservation_url");
                return;
            } 
        } catch (error) {
            console.error("Błąd podczas sprawdzania dostępności miejsc:", error);
            alert("Wystąpił problem z weryfikacją miejsc. Spróbuj ponownie później.");
        }

        try {
            const today = new Date();
            const year = today.getFullYear();
            const month = String(today.getMonth() + 1).padStart(2, '0'); // miesiące są od 0 do 11
            const day = String(today.getDate()).padStart(2, '0');

            const formattedDate = `${year}-${month}-${day}`;
            const transactionData = {
                id_users: parseInt(sessionStorage.getItem("userId")),
                id_showings: parseInt(showing_id),
                status: "pending",
                date: formattedDate
            };
            const response_transaction_send = await fetch("http://localhost:8000/reservations/transactions", {
            method: "POST",
            headers: {
                'Authorization': `Bearer ${token}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify(transactionData),
            });
            if (response_transaction_send.status === 401) {
                alert("Unauthorized. Please log in again.");
                window.location.href = "login.html";
            }
            if (response_transaction_send.status === 401) {
                alert("Unauthorized. Please log in again.");
                window.location.href = "login.html";
                return;
            }
            if (!response_transaction_send.ok) throw new Error("Błąd podczas tworzenia transakcji.");

            const transaction_sent = await response_transaction_send.json();
            const transaction_id = transaction_sent.transaction_id

            sessionStorage.setItem("transactionId", transaction_id);
            const paymentUrl = `payment.html?transaction_id=${encodeURIComponent(transaction_id)}`;

            const seatPriceMap = JSON.parse(sessionStorage.getItem("seatPriceMap")) || {};
            const ticketsData = storedSeats_ids.map(seatId => {
                const priceType = seatPriceMap[seatId];
                const priceId = priceTypeToId[priceType];
                return {
                    id_transaction: parseInt(transaction_id),
                    id_pricelist: parseInt(priceId),
                    id_seats: parseInt(seatId)
                };
            });
            
            try {
            const response_ticket_creation = await fetch("http://localhost:8000/reservations/tickets/bulk", {
            method: "POST",
            headers: {
                'Authorization': `Bearer ${token}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify(ticketsData),
            });

            if (response_ticket_creation.status === 401) {
                alert("Unauthorized. Please log in again.");
                window.location.href = "login.html";
                return;
            }
            if (!response_ticket_creation.ok) throw new Error("Błąd podczas tworzenia biletów.");
            sessionStorage.setItem("ticketsData", JSON.stringify(ticketsData));
            window.location.href = paymentUrl;
            } catch (error) {console.error("Błąd podczas tworzenia transakcji:", error);
                alert("Wystąpił problem z dodaniem biletu. Spróbuj ponownie później.");
            }
        }   catch (error) {
                console.error("Błąd podczas tworzenia transakcji:", error);
                alert("Wystąpił problem z utworzeniem twojej transakcji lub dodaniem biletu. Spróbuj ponownie później.");
        }
});
}

function updatePriceMapping(seatId, type) {
    let seatPriceMap = JSON.parse(sessionStorage.getItem("seatPriceMap")) || {};
    seatPriceMap[seatId] = type;
    sessionStorage.setItem("seatPriceMap", JSON.stringify(seatPriceMap));
}

function normalizeTickets(tickets) {
    return tickets.map(ticket => ({
        id_pricelist: ticket.id_pricelist,
        id_transaction: ticket.id_transaction,
        id_seats: ticket.id_seat || ticket.id_seats
    }));
}

function areArraysEqualIgnoringId(arr1, arr2) {
  if (arr1.length !== arr2.length) return false;

  return arr1.every((obj1, index) => {
    const obj2 = arr2[index];
    const cleanedObj1 = {
      id_pricelist: obj1.id_pricelist,
      id_transaction: obj1.id_transaction,
      id_seats: obj1.id_seats
    };

    return (
      cleanedObj1.id_pricelist === obj2.id_pricelist &&
      cleanedObj1.id_transaction === obj2.id_transaction &&
      cleanedObj1.id_seats === obj2.id_seats
    );
  });
}

window.addEventListener("load", loadOrderPage);