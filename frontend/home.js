let chosenDate = null;
let chosenDate_id = null;
const day_labels = ['Nd', 'Pn', 'Wt', 'Śr', 'Czw', 'Pt', 'Sb']

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
        btn.innerText = day_labels[Date(day.date).getDay()];
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
    const res = await fetch(`http://localhost:8000/showings/showings/by-date/${date_id}`);
    const screenings = await res.json();
    const movs = await fetch(`http://localhost:8000/movies/0`);
    const movies_fetch = await movs.json();
    const movies_dict = {};

    movies_fetch.forEach(m => {
        movies_dict[m.id].push(m.tittle);
    });

    const filmsContainer = document.getElementById("films");
    filmsContainer.innerHTML = "";
    //date format
    const dateObj = new Date(date);
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    
    const grouped = {};
    screenings.forEach(s => {
        if (!grouped[movies_dict[s.id_movies]]) {
            grouped[movies_dict[s.id_movies]] = [];
        }
        grouped[movies_dict[s.id_movies]].push([(s.hour).slice(0, 5), s.id_hall, s.id]);
    });

    for (const title in grouped) {
        const section = document.createElement("section");
        section.className = "film";

        section.innerHTML = `
            <img src="https://via.placeholder.com/150x220.png?text=${encodeURIComponent(title)}" alt="${title}" />
            <div class="info">
                <h2>${title}</h2>
                <div class="showtimes">

                    ${grouped[title].map(([time, hall_id, showing_id]) => `
                        <button onclick="goToReservation('${title}', '${time}', '${formattedDate}','${date_id}','${hall_id}, '${showing_id}')">${time}</button>
                    `).join('')}
                </div>
            </div>
        `;
        filmsContainer.appendChild(section);
    }
}

function goToReservation(filmTitle, time, date, date_id, hall_id, showing_id) {
    const url = `reservation.html?film=${encodeURIComponent(filmTitle)}&time=${encodeURIComponent(time)}&date=${encodeURIComponent(date)}&date_id=${encodeURIComponent(date_id)}&hall_id=${encodeURIComponent(hall_id)}&showing_id=${encodeURIComponent(showing_id)}`;
    window.location.href = url;
}

window.onload = loadDays;