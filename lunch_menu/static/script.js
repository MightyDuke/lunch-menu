import Alpine from "/static/alpine.min.js"

window.locale = "cs-cz";

function isoDate(date) {
    return `${date.getFullYear().toString().padStart(4, "0")}-` +
        `${(date.getMonth() + 1).toString().padStart(2, "0")}-` + 
        `${date.getDate().toString().padStart(2, "0")}`
}

window.getDaysInWeek = function() {
    const now = new Date;
    const result = [];

    for (let i = 0; i < 5; i++) {
        let date = new Date;
        date.setDate(now.getDate() - now.getDay() + 1 + i);
        result.push(isoDate(date));
    }

    return result;
}

window.getLocalizedWeekName = function(date) {
    const parsedDate = new Date(Date.parse(date));
    return parsedDate.toLocaleDateString(window.locale, { weekday: "long" });
}

window.getLocalizedLongFormat = function(date) {
    const parsedDate = new Date(Date.parse(date));
    return parsedDate.toLocaleDateString(window.locale, { year: "numeric", month: "long", day: "numeric" });
}

document.addEventListener("alpine:init", () => {
    Alpine.data("app", () => ({
        locale: "cs-cz",
        selectedDate: null,
        providers: [],

        async init() {
            this.selectedDate = isoDate(new Date);

            const response = await fetch("/api/providers");
            this.providers = await response.json();
        }
    }));

    Alpine.data("provider", (provider = null) => ({
        provider: null,

        async init() {
            const response = await fetch(`/api/providers/${provider}`);
            this.provider = await response.json();
        }
    }));
});

Alpine.start();