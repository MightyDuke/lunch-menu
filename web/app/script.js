import Alpine from "/node_modules/alpinejs/dist/module.esm.js"
import persist from "/node_modules/@alpinejs/persist/dist/module.esm.js"

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

window.isPwa = () => {
    return window?.matchMedia("(display-mode: standalone)").matches ?? false;
}

document.addEventListener("alpine:init", () => {
    Alpine.data("app", () => ({
        selectedDate: null,
        establishments: [],
        token: Alpine.$persist(null),
        user: null,
        menuOpen: false,
        votes: {},

        async init() {
            google.accounts.id.initialize({
                client_id: "463687060136-g6v6qjf7r1jh49lfpeogq3qm5rj7islk.apps.googleusercontent.com",
                callback: async response => {
                    await this.fetchSession(response);
                    await this.fetchUser();
                }
            });

            google.accounts.id.renderButton(
                document.getElementById("google-login"),
                { 
                    locale: "cs",
                    theme: "filled_black",
                    size: "medium" 
                }
            );

            this.selectedDate = isoDate(new Date);

            const response = await fetch("/api/establishments");
            this.establishments = await response.json();

            this.voteStream = new EventSource("/api/vote/stream");
            this.voteStream.onmessage = (event) => {
                const votes = JSON.parse(event.data);
                this.votes = votes;
            };

            if (this.token != null) {
                await this.fetchUser();
            }
        },

        toggleMenu() {
            this.menuOpen = !this.menuOpen;
        },

        async fetchSession(data) {
            let response = await fetch("/api/user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "id_token": data.credential
                })
            });

            response = await response.json();
            this.token = response.token;

            await this.fetchUser();
        },

        async fetchUser() {
            let response = await fetch("/api/user", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            });

            response = await response.json();
            this.user = response;
        },

        async logout() {
            let response = await fetch("/api/user", {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${this.token}`
                }
            });

            this.token = null;
            this.user = null;
        },

        async vote(path) {
            if (this.token == null) {
                return;
            }

            let response = await fetch("/api/vote", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    "path": path
                })
            });
        }
    }));

    Alpine.data("menu", (establishment = null) => ({
        menu: null,

        async init() {
            const response = await fetch(`/api/establishments/${establishment}`);
            this.menu = await response.json();
        }
    }));
});

window.Alpine = Alpine;

Alpine.plugin(persist);
Alpine.start();