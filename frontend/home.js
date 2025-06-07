let chosenDate = null;
let chosenDate_id = null;
const day_labels = ['Nd', 'Pn', 'Wt', 'Śr', 'Czw', 'Pt', 'Sb'];

async function loadDays() {
    const res = await fetch("http://localhost:8000/cur_week");
    const days = await res.json();
    const dayButtons = document.getElementById("day-buttons");
    dayButtons.innerHTML = "";

    const params = new URLSearchParams(window.location.search);
    chosenDate = params.get("date") || days[0].date;
    chosenDate_id = params.get("id") || days[0].id;

    days.forEach(day => {
        const btn = document.createElement("button");
        btn.className = "day-button";
        btn.innerText = day_labels[new Date(day.date).getDay()];
        if (day.date === chosenDate) {
            btn.classList.add("active");
        }
        btn.onclick = () => {
            window.location.href = `home.html?date=${day.date}&id=${day.id}`;
        };
        dayButtons.appendChild(btn);
    });

    loadFilms(chosenDate, chosenDate_id);
}

async function loadFilms(date, date_id) {
    let screenings;
    try {
        const res = await fetch(`http://localhost:8000/showings/showings/by-date/${date_id}`);
        if (!res.ok) throw new Error("Błąd podczas pobierania seansów");
        screenings = await res.json();
    } catch (err) {
        console.error("Nie udało się pobrać seansów:", err);
        document.getElementById("films").innerHTML = "<p class='error'>Brak seansów dla wybranego dnia.</p>";
        return;
    }

    const movies_dict = {};

    // Pobierz unikalne ID filmów
    const movieIds = [...new Set(screenings.map(s => s.id_movies))];

    // Pobierz tytuły filmów dla każdego ID
    for (const movieId of movieIds) {
        try {
            const res = await fetch(`http://localhost:8000/movies/movies/${movieId}`);
            if (!res.ok) throw new Error(`Film ${movieId} nie znaleziony`);
            const movie = await res.json();
            movies_dict[movieId] = movie.title || movie.tittle || "Nieznany tytuł";
        } catch (err) {
            console.warn("Błąd przy pobieraniu filmu:", movieId, err);
            movies_dict[movieId] = "Nieznany tytuł";
        }
    }

    const filmsContainer = document.getElementById("films");
    filmsContainer.innerHTML = "";

    const dateObj = new Date(date);
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;

    const grouped = {};
    screenings.forEach(s => {
        const movieTitle = movies_dict[s.id_movies];
        if (!movieTitle) return;

        if (!grouped[movieTitle]) {
            grouped[movieTitle] = [];
        }
        grouped[movieTitle].push([(s.hour || '').slice(0, 5), s.id_hall, s.id, s.id_movies]);
    });

    if (Object.keys(grouped).length === 0) {
        filmsContainer.innerHTML = "<p class='info'>Brak dostępnych seansów w wybranym dniu.</p>";
        return;
    }

    for (const title in grouped) {
        const section = document.createElement("section");
        section.className = "film";
        section.innerHTML = `
            <img src="./imgs/${grouped[title][0][3]}.png" alt="${title}" />
            <div class="info">
                <h2>${title}</h2>
                <div class="showtimes">
                    ${grouped[title].map(([time, hall_id, showing_id, movie_id]) => `
                        <button onclick="goToReservation('${title}', '${time}', '${formattedDate}', '${date_id}', '${hall_id}', '${showing_id}')">${time}</button>
                    `).join('')}
                </div>
            </div>
        `;
        filmsContainer.appendChild(section);
    }
}



function goToReservation(filmTitle, time, date, date_id, hall_id, showing_id) {
  const login = sessionStorage.getItem("userLogin");
  if (!login) {
    // przekierowanie po loginie
    const redirectUrl = encodeURIComponent(
      `reservation.html?film=${filmTitle}&time=${time}&date=${date}&date_id=${date_id}&hall_id=${hall_id}&showing_id=${showing_id}`
    );
    window.location.href = `login.html?redirect=${redirectUrl}`;
    return;
  }

  const url = `reservation.html?film=${encodeURIComponent(filmTitle)}&time=${encodeURIComponent(time)}&date=${encodeURIComponent(date)}&date_id=${encodeURIComponent(date_id)}&hall_id=${encodeURIComponent(hall_id)}&showing_id=${encodeURIComponent(showing_id)}`;
  window.location.href = url;
}

window.addEventListener("load", loadDays);
