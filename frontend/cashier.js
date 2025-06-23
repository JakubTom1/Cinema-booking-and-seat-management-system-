window.addEventListener("DOMContentLoaded", async () => {
    const token = sessionStorage.getItem("access_token");
    const userId = sessionStorage.getItem("userId");
    const container = document.getElementById("transactions-container");
    document.getElementById("backButton").addEventListener("click", () => {
        const lastPage = sessionStorage.getItem("lastPage") || "home.html";
        window.location.href = lastPage;
    });

    document.getElementById("homeButton").addEventListener("click", () => {
        window.location.href = "home.html";
    });
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

    for (const transaction of transactions) {
        if (transaction.total_price != 0) {
            const div = document.createElement("div");
            div.className = "transaction";
            div.innerHTML = `
                <h3>${transaction.movie_title}</h3>
                <p>Data transakcji: ${transaction.transaction_date}</p>
                <p>Data seansu: ${transaction.date} ${transaction.time}</p>
                <p>Numer sali: ${transaction.hall_number}</p>
                <p>Miejsca: ${transaction.seats.map(s => `Rząd ${s.row}, Miejsce ${s.number}`).join(", ") || "Brak"}</p>
                <p>Status: ${transaction.status}</p>
                <p>Kwota: ${transaction.total_price} zł</p>
            `;

            const now = new Date();
            const screeningDateTime = new Date(`${transaction.date}T${transaction.time}`);

            if (transaction.status === "realized" && screeningDateTime > now) {
                const refundBtn = document.createElement("button");
                refundBtn.textContent = "Usuń";
                refundBtn.classList.add("panel-btn");

                refundBtn.addEventListener("click", async () => {
                    try {
                        const res = await fetch(`http://localhost:8000/reservations/transactions/${transaction.transaction_id}/cancel`, {
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
            } else if (transaction.status === "pending" && screeningDateTime > now) {
                const payBtn = document.createElement("button");
                payBtn.textContent = "Zapłata";
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
    }}
});