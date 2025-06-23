window.addEventListener("load", async () => {
    const container = document.getElementById("transactionsContainer");
    const token = sessionStorage.getItem("access_token");
    const userId = sessionStorage.getItem("userId");
    document.getElementById("backButton").addEventListener("click", () => {
        const lastPage = sessionStorage.getItem("lastPage") || "home.html";
        window.location.href = lastPage;
    });

    document.getElementById("homeButton").addEventListener("click", () => {
        window.location.href = "home.html";
    });
    if (!token || !userId) {
        alert("Zaloguj się, aby zobaczyć bilety.");
        window.location.href = "login.html";
        return;
    }

    try {
        const res = await fetch("http://localhost:8000/reservations/user/transactions", {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (res.status === 401) {
            alert("Unauthorized. Please log in again.");
            window.location.href = "login.html";
        }
        if (!res.ok) throw new Error("Nie udało się pobrać danych.");

        const transactions = await res.json();

        transactions.sort((a, b) => new Date(b.transaction_date) - new Date(a.transaction_date));

        transactions.forEach(transaction => {
            if (transaction.total_price != 0) {
                const div = document.createElement("div");
                div.className = "transaction";

                const showingDate = new Date(`${transaction.date}T${transaction.time}`);
                const now = new Date();
                const nowPlus15Min = new Date(now.getTime() + 15 * 60 * 1000);
                const seatsText = transaction.seats.length > 0
                    ? transaction.seats.map(seat => `Rząd ${seat.row}, Miejsce ${seat.number}`).join("; ")
                    : "Brak miejsc";

                div.innerHTML = `
                    <h3>${transaction.movie_title}</h3>
                    <p>Data transakcji: ${transaction.transaction_date}</p>
                    <p>Data seansu: ${transaction.date} ${transaction.time}</p>
                    <p>Sala: ${transaction.hall_number}</p>
                    <p>Miejsca: ${seatsText}</p>
                    <p>Status: ${transaction.status}</p>
                    <p>Łączna kwota: ${transaction.total_price} zł</p>
                `;

                if (transaction.status === "realized" && showingDate > nowPlus15Min) {
                    const refundBtn = document.createElement("button");
                    refundBtn.textContent = "Zwrot";
                    refundBtn.classList.add("panel-btn");
                    refundBtn.addEventListener("click", async () => {
                        const token = sessionStorage.getItem("access_token");
                        const transactionId = transaction.transaction_id;

                        try {
                            const res = await fetch(`http://localhost:8000/reservations/transactions/${transactionId}/cancel`, {
                                method: "DELETE",
                                headers: {
                                    'Authorization': `Bearer ${token}`
                                }
                            });
                            if (res.status === 401) {
                                alert("Unauthorized. Please log in again.");
                                window.location.href = "login.html";
                            }
                            if (!res.ok) throw new Error("Nie udało się anulować biletów.");
                            alert("Bilety zostały zwrócone.");
                            window.location.reload();

                        } catch (error) {
                            alert("Błąd podczas zwrotu: " + error.message);
                        }
                    });
                    div.appendChild(refundBtn);
                } else if (transaction.status === "pending" && showingDate > now) {
                    const payBtn = document.createElement("button");
                    payBtn.textContent = "Opłać";
                    payBtn.classList.add("panel-btn");
                    payBtn.addEventListener("click", () => {
                        sessionStorage.setItem("transactionId", transaction.transaction_id);
                        sessionStorage.setItem("total_payment", transaction.total_price);
                        const paymentUrl = `payment.html?transaction_id=${encodeURIComponent(transaction.transaction_id)}`;
                        window.location.href = paymentUrl;
                    });
                    div.appendChild(payBtn);
                } else {
                    const info = document.createElement("p");
                    info.textContent = "Seans zakończony lub transakcja anulowana.";
                    div.appendChild(info);
                }

                container.appendChild(div);
            }
        });

    } catch (error) {
        console.error("Błąd:", error);
        alert("Wystąpił błąd przy pobieraniu transakcji. Zaloguj się ponownie");
        logout();
    }
});

function logout() {
  sessionStorage.clear();
  window.location.href = "home.html";
}