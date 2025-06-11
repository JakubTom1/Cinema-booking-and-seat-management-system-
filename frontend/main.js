function updateUserDisplay() {
  const userDisplay = document.getElementById("userDisplay");
  const login = sessionStorage.getItem("userLogin");
  const userStatus = parseInt(sessionStorage.getItem("userStatus")); // 0, 1, 2

  if (login) {
    let panelButton = "";
    if (userStatus === 0) {
      panelButton = `<button onclick="window.location.href='admin_page.html'" class="panel-btn">Panel administratora</button>`;
    } else if (userStatus === 1) {
      panelButton = `<button onclick="window.location.href='cashier.html'" class="panel-btn">Panel sprzedawcy</button>`;
    } else if (userStatus === 2) {
      panelButton = `<button onclick="window.location.href='client.html'" class="panel-btn">Twoje bilety</button>`;
    }
    userDisplay.innerHTML = `
    <div class="user-info">
        <span>Zalogowany jako: <strong class="user-name">${login}</strong></span>
    </div>
    <div class="user-buttons">
        ${panelButton}
        <button onclick="logout()" class="logout">Wyloguj</button>
    </div>
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