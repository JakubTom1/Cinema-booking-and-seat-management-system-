const days = {
            "Pn": "2025-05-12",
            "Wt": "2025-05-13",
            "Śr": "2025-05-14",
            "Czw": "2025-05-15",
            "Pt": "2025-05-16"
        };
        
let params = new URLSearchParams(window.location.search);
if (!params.has("date")) {
    selectDay('Pn')
    params = new URLSearchParams(window.location.search);
}
let chosenDate = params.get("date");

function goToReservation(filmTitle, time, date) {
    const url = `reservation.html?film=${encodeURIComponent(filmTitle)}&time=${encodeURIComponent(time)}&date=${encodeURIComponent(date)}`;
    window.location.href = url;
}



function selectDay(dayLabel) {
    const date = days[dayLabel];
    if (date) {
        window.location.href = `home.html?date=${date}`;
    }
    params = new URLSearchParams(window.location.search);
    chosenDate = params.get("date");
}

document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const currentDate = params.get("date");
    const buttons = document.querySelectorAll(".day-button");
    buttons.forEach(btn => {
        if (days[btn.innerText] === currentDate) {
        btn.classList.add("active");
        }
    });
});