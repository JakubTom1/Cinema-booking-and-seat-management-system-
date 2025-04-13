async function pobierzFilmy() {
    let response = await fetch("http://127.0.0.1:8000/seanse");
    let filmy = await response.json();
    let lista = document.getElementById("lista-filmow");
    filmy.forEach(film => {
        let li = document.createElement("li");
        li.innerText = film.title;
        lista.appendChild(li);
    });
}
window.onload = pobierzFilmy;