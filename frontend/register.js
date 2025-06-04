document.getElementById("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    first_name: document.getElementById("first_name").value,
    last_name: document.getElementById("last_name").value,
    login: document.getElementById("login").value,
    password: document.getElementById("password").value,
  };

  try {
    const res = await fetch("http://localhost:8000/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!res.ok) throw new Error("Nie udało się zarejestrować");

    alert("Rejestracja zakończona sukcesem. Możesz się teraz zalogować.");
    window.location.href = "login.html";
  } catch (err) {
    alert(err.message);
  }
});