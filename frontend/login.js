document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("http://localhost:8000/auth/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: username,
          password: password,
        }),
      });

      if (!response.ok) throw new Error("Błędny login lub hasło");

      const data = await response.json();
      sessionStorage.setItem("access_token", data.access_token);
      sessionStorage.setItem("userLogin", username);
      sessionStorage.setItem("userStatus", data.user_status);

      const params = new URLSearchParams(window.location.search);
      const redirect = params.get("redirect") || "home.html";
      window.location.href = redirect;
    } catch (err) {
      alert(err.message);
    }
  });
});