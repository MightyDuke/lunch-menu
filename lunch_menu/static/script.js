import Alpine from "https://cdnjs.cloudflare.com/ajax/libs/alpinejs/3.14.8/module.esm.min.js"

document.addEventListener("alpine:init", () => {
    function isoDate(date) {
        return `${date.getFullYear().toString().padStart(4, "0")}-` +
            `${(date.getMonth() + 1).toString().padStart(2, "0")}-` + 
            `${date.getDate().toString().padStart(2, "0")}`;
    }

    Alpine.data("app", () => ({
        locale: "cs-cz",
        activeDay: null,
        days: [],
        providers: [],

        async init() {
            const now = new Date;

            for (let i = 0; i < 7; i++) {
                const date = new Date;
                date.setDate(now.getDate() - now.getDay() + 1 + i);

                const day = {
                    "iso": isoDate(date),
                    "weekday": date.toLocaleDateString(this.locale, { weekday: "long" }),
                    "date": date.toLocaleDateString(this.locale, { year: "numeric", month: "long", day: "numeric" }),
                    "active": i != 5 && i != 6
                };

                this.days.push(day);

                if (day.iso === isoDate(now)) {
                    this.activeDay = day;
                }
            }

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