function updateUserDisplay() {
  const userDisplay = document.getElementById("userDisplay");
  const login = sessionStorage.getItem("userLogin");

  if (login) {
    userDisplay.innerHTML = `
      <span>Zalogowany jako: <strong>${login}</strong></span>
      <button onclick="logout()" class="logout">Wyloguj</button>
    `;
  } else {
    userDisplay.innerHTML = `
      <button onclick="window.location.href='login.html'" class="login">Login</button>
    `;
  }
}

function logout() {
  sessionStorage.clear();
  window.location.href = "home.html";
}

window.addEventListener("load", updateUserDisplay);