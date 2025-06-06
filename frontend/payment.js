window.addEventListener("load", () => {
    const totalDisplay = document.querySelector("#formularz p strong");
    const total = JSON.parse(sessionStorage.getItem("total_payment")) || 0;
    totalDisplay.textContent = `${total} zł`;

    const params = new URLSearchParams(window.location.search);
    const transaction_id = params.get("transaction_id");

    const paymentForm = document.querySelector("form");
    paymentForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const selectedMethod = document.querySelector("input[name='metoda']:checked")?.value;
        if (!selectedMethod) {
            alert("Wybierz metodę płatności.");
            return;
        }
        /*
        try {
            const token = sessionStorage.getItem("access_token");
            const res = await fetch(`http://localhost:8000/transactions/confirm`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    transaction_id: transaction_id,
                    payment_method: selectedMethod,
                    amount_paid: total
                })
            });

            if (!res.ok) {
                const errMsg = await res.text();
                throw new Error(`Błąd przy potwierdzaniu płatności: ${errMsg}`);
            }

            // On success: show confirmation, hide form, clear reservation data
            document.getElementById("potwierdzenie").style.display = "block";
            document.getElementById("formularz").style.display = "none";
            for (let i = sessionStorage.length - 1; i >= 0; i--) {
            const key = sessionStorage.key(i);
            if (key !== "access_token" && key !== "userLogin") {
                sessionStorage.removeItem(key);
            }
        }
        } catch (err) {
            alert(err.message);
            console.error(err);
        }
            */
        document.getElementById("potwierdzenie").style.display = "block";
        document.getElementById("formularz").style.display = "none";
        for (let i = sessionStorage.length - 1; i >= 0; i--) {
            const key = sessionStorage.key(i);
            if (key !== "access_token" && key !== "userLogin") {
                sessionStorage.removeItem(key);
            }
        }
    });
});