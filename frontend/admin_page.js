window.addEventListener("DOMContentLoaded", async () => {
    const token = sessionStorage.getItem("access_token");

    const movieSelect = document.getElementById("movie-select");
    const dateSelect = document.getElementById("date-select");
    const addForm = document.getElementById("add-showing-form");
    const deleteForm = document.getElementById("delete-showing-form");

    document.getElementById("backButton").addEventListener("click", () => {
        const lastPage = sessionStorage.getItem("lastPage") || "home.html";
        window.location.href = lastPage;
    });

    document.getElementById("homeButton").addEventListener("click", () => {
        window.location.href = "home.html";
    });
    const maxMovieId = 10;
    for (let id = 1; id <= maxMovieId; id++) {
        try {
        const res = await fetch(`http://localhost:8000/movies/movies/${id}`);
        if (!res.ok) continue;

        const movie = await res.json();
        const option = document.createElement("option");
        option.value = movie.id;
        option.textContent = movie.tittle;
        movieSelect.appendChild(option);
    } catch (err) {
        console.error("Błąd przy pobieraniu filmu:", err);
    }
  }


    const res = await fetch("http://localhost:8000/cur_week");
    const days = await res.json();
    days.forEach(day => {
    const option = document.createElement("option");
    option.value = day.id;
    const date = new Date(day.date);
    option.textContent = date.toLocaleDateString("pl-PL", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric"
    });
    dateSelect.appendChild(option);
    });


    addForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const id_movies = parseInt(movieSelect.value);
    const id_hall = parseInt(document.getElementById("hall-input").value);
    const id_date = parseInt(dateSelect.value);
    const hourRaw = document.getElementById("hour-input").value;

    if (id_hall < 1 || id_hall > 5) {
        return alert("Numer sali musi być w zakresie od 1 do 5.");
    }

    const hour = `${hourRaw}:00.000Z`;

    const payload = {
        id_movies,
        id_hall,
        id_date,
        hour
    };

    try {
        const response = await fetch("http://localhost:8000/admin/admin/showings", {
        method: "POST",
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
            throw new Error("Nie udało się dodać seansu.");
      }

      alert("Seans dodany pomyślnie!");
      addForm.reset();
    } catch (error) {
        alert("Błąd: " + error.message);
    }
    });


    deleteForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const showingId = document.getElementById("delete-id-input").value;

        try {
            const res = await fetch(`http://localhost:8000/admin/admin/showings/${showingId}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${token}` }
        });

        if (!res.ok) throw new Error("Nie udało się usunąć seansu.");

        alert("Seans usunięty pomyślnie.");
        deleteForm.reset();
        } catch (error) {
        alert("Błąd: " + error.message);
        }
    });
});