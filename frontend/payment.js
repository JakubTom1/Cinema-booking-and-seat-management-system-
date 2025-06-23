window.addEventListener("load", () => {
    const totalDisplay = document.querySelector("#formularz p strong");
    const total = JSON.parse(sessionStorage.getItem("total_payment")) || 0;
    totalDisplay.textContent = `${total} zł`;
    sessionStorage.setItem("payment_url", window.location.href);
    sessionStorage.setItem("lastPage", window.location.href);
    const params = new URLSearchParams(window.location.search);
    const transaction_id = parseInt(params.get("transaction_id"));
    const transaction_id_session = parseInt(sessionStorage.getItem("transactionId"));
    if (transaction_id !== transaction_id_session) {
        for (let i = sessionStorage.length - 1; i >= 0; i--) {
            const key = sessionStorage.key(i);
            if (key !== "access_token" && key !== "userLogin" && key !== "userStatus" && key !== "userId") {
                sessionStorage.removeItem(key);
            }
        }
        alert('Wystąpił błąd zgodności statusu płatności. Powrót na stronę główną');
        window.location.href = "home.html";
    }   
    const paymentForm = document.querySelector("form");
    paymentForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const selectedMethod = document.querySelector("input[name='metoda']:checked")?.value;
        if (!selectedMethod) {
            alert("Wybierz metodę płatności.");
            return;
        }
        try {
            const token = sessionStorage.getItem("access_token");
            const res = await fetch(`http://localhost:8000/reservations/transactions/${transaction_id}`, {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    transaction_id: transaction_id
                })
            });
            if (res.status === 401) {
                alert("Unauthorized. Please log in again.");
                window.location.href = "login.html";
            }
            if (!res.ok) {
                const errMsg = await res.text();
                alert(`Błąd przy potwierdzaniu płatności: ${errMsg}`);
                logout();
                window.location.href = "home.html";
            }

            document.getElementById("potwierdzenie").style.display = "block";
            document.getElementById("formularz").style.display = "none";
            for (let i = sessionStorage.length - 1; i >= 0; i--) {
            const key = sessionStorage.key(i);
            if (key !== "access_token" && key !== "userLogin" && key !== "userStatus" && key !== "userId") {
                sessionStorage.removeItem(key);
                }
            }
        } catch (err) {
            alert(err.message);
            console.error(err);
        }

    });
});
