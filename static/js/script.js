import Alpine from "/static/js/alpine.min.js"

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

window.getLocalizedLongFormat = date => {
    const parsedDate = new Date(Date.parse(date));
    return parsedDate.toLocaleDateString(window.locale, { year: "numeric", month: "long", day: "numeric" });
}

window.randomInterval = (min, max) => {
    return Math.random() * (max - min) + min;
}

document.addEventListener("alpine:init", () => {
    Alpine.data("app", () => ({
        selectedDate: null,
        providers: [],
        tab: "menu",

        async init() {
            this.selectedDate = isoDate(new Date);

            const response = await fetch("/api/providers");
            this.providers = await response.json();
        },

        switchTab(name) {
            this.tab = name;
        }
    }));

    Alpine.data("menu", (provider = null) => ({
        provider: null,

        async init() {
            const response = await fetch(`/api/providers/${provider}`);
            this.provider = await response.json();
        }
    }));

    Alpine.data("wheel", () => ({
        options: [],
        pending: false,
        lastUpdate: null,

        angle: 0,
        momentum: 0,

        init() {
            const callback = (timestamp) => {
                if (this.lastUpdate == null) {
                    this.lastUpdate = timestamp;
                }

                const delta = (timestamp - this.lastUpdate) / (1000 / 60);
                this.lastUpdate = timestamp;

                this.angle += this.momentum * delta;
                this.momentum *= 0.995;

                if (this.momentum < 0.05) {
                    this.momentum = 0;
                    this.pending = false;
                } else {
                    this.pending = true;
                }

                window.requestAnimationFrame(callback);
            };

            window.requestAnimationFrame(callback);
        },

        toggleOption(name) {
            this.options.push(name);
        },

        spin() {
            this.momentum = randomInterval(7, 13);
        }
    }));
});

window.Alpine = Alpine;
Alpine.start();