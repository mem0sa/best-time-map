let map;
let activePlaceId = null;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat:56.839448, lng:60.597636 },
        zoom: 14,
    });

    map.addListener("click", (event) => {
        if (event.placeId) {
            event.stop();
            handlePlaceClick(event.placeId);
        }
    });
}

function handlePlaceClick(placeId) {
    activePlaceId = placeId;

    fetch('/api/place-details/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ place_id: placeId })
    })
    .then(res => res.json())
    .then(data => {
        showPlaceDetails(data.details);
        showRecommendation(data.recommendation);
    })
    .catch(() => {
        activePlaceId = null;
    });
}

function showPlaceDetails(details) {
    const panel = document.getElementById("details");

    panel.innerHTML = `
        <h3>${details.name}</h3>
        <p>${details.address}</p>
        <p><strong>Рейтинг:</strong> ${details.rating ?? '—'}</p>
    `;

    panel.style.display = "block";
}

function getColorRelative(score, min, max) {
    const ratio = (score - min) / (max - min);
    const r = Math.floor(ratio * 255);
    const g = Math.floor((1 - ratio) * 255);
    const b = 0;
    return `rgb(${r},${g},${b})`;
}

function showRecommendation(data) {
    const panel = document.querySelector(".recommendation-panel-inner");
    const heatmap = data.table;
    const best = data.best_time;
    const worst = data.worst_time;
    const best_weekends = data.best_time_on_weekends;

    const days = [
        "Понедельник",
        "Вторник",
        "Среда",
        "Четверг",
        "Пятница",
        "Суббота",
        "Воскресенье"
    ];
    let html = `<button onclick="closeRecommendation()" class="close-button">×</button>`
    html += `<h4>Тепловая карта посещаемости</h4>`;
    html += `<table class="heatmap-table">`;
    html += `<tr><th></th>`;
    days.forEach(day => html += `<th>${day}</th>`);
    html += `</tr>`;

    for (const hourLabel in heatmap) {
        const hourNumber = parseInt(hourLabel);

        html += `<tr>`;
        html += `<td class="hour-cell">${hourLabel}</td>`;

        days.forEach(day => {
            const score = heatmap[hourLabel][day];

            const color = getColorRelative(score, best["score"], worst["score"]);

            const isBest =
                score < (best["score"] + 3) || ((day == "Суббота" || day == "Воскресенье") && score < (best_weekends["score"] + 2))
                    ? "best-cell"
                    : "";

            html += `<td class="${isBest}" style="background-color: ${color}; color: ${score > 50 ? '#fff' : '#000'}">${score}</td>`;
        });

        html += `</tr>`;
    }

    html += `</table>`;

    html += `
        <div class="best-day">
            Лучшее время: ${best.day}, ${best.hour}:00
        </div>
        <div class="best-day">
            Лучшее время на выходных: ${best_weekends.day}, ${best_weekends.hour}:00
        </div>
    `;

    panel.innerHTML = html;
    const whole_panel = document.querySelector(".recommendation-panel");
    whole_panel.classList.add("open");
}

function closeRecommendation(){
    const whole_panel = document.querySelector(".recommendation-panel");
    whole_panel.classList.remove("open");
}