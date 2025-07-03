import Alpine from "/node_modules/alpinejs/dist/module.esm.js"

window.locale = "cs";

window.isoDate = date => {
    return `${date.getFullYear().toString().padStart(4, "0")}-` +
        `${(date.getMonth() + 1).toString().padStart(2, "0")}-` + 
        `${date.getDate().toString().padStart(2, "0")}`
}

window.capitalize = text => {
    return text[0].toUpperCase() + text.slice(1);
}

window.getDaysInWeek = () => {
    const now = new Date;
    const result = [];

    for (let i = 0; i < 5; i++) {
        let date = new Date;
        date.setDate(now.getDate() - now.getDay() + 1 + i);
        result.push(isoDate(date));
    }

    return result;
}

window.getLocalizedWeekName = date => {
    const parsedDate = new Date(Date.parse(date));
    return parsedDate.toLocaleDateString(window.locale, { weekday: "long" });
}

window.getLocalizedLongFormatDate = date => {
    const parsedDate = new Date(Date.parse(date));
    return parsedDate.toLocaleDateString(window.locale, { year: "numeric", month: "long", day: "numeric" });
}

document.addEventListener("alpine:init", () => {
    Alpine.data("app", () => ({
        selectedDate: null,
        providers: [],

        async init() {
            this.selectedDate = isoDate(new Date);

            const response = await fetch("/api/providers");
            this.providers = await response.json();
        },
    }));

    Alpine.data("menu", (provider = null) => ({
        menu: null,

        async init() {
            const response = await fetch(`/api/providers/${provider}`);
            this.menu = await response.json();
        }
    }));
});

window.Alpine = Alpine;
Alpine.start();