import Alpine from "/node_modules/alpinejs/dist/module.esm.js"
import persist from "/node_modules/@alpinejs/persist/dist/module.esm.js"

window.locale = "cs";

window.getIsoDate = date => {
    return `${date.getFullYear().toString().padStart(4, "0")}-` +
        `${(date.getMonth() + 1).toString().padStart(2, "0")}-` + 
        `${date.getDate().toString().padStart(2, "0")}`
}

window.getDaysInWeek = () => {
    const now = new Date;
    const result = [];

    for (let i = 0; i < 5; i++) {
        let date = new Date;
        date.setDate(now.getDate() - now.getDay() + 1 + i);

        result.push(getIsoDate(date));
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

window.chain = (...items) => {
    const result = [];

    for (let item of items) {
        if (item !== undefined) {
            result.push(...item);
        }
    }

    return result;
}

document.addEventListener("alpine:init", () => {
    Alpine.data("app", () => ({
        selectedDate: null,
        establishments: [],
        votes: {},
        
        session: Alpine.$persist(null).as("session"),
        user: null,

        async init() {
            this.selectedDate = getIsoDate(new Date);
            
            if (this.session != null) {
                try {
                    await this.fetchProfile();
                } catch {
                    this.user = null;
                }
            }

            window.sendSessionToken = token => this.startSession(token);

            this.voteStream = new EventSource("/api/vote/stream");
            this.voteStream.onmessage = (event) => this.votes = { ...this.votes, ...JSON.parse(event.data) };

            const response = await this.fetch("GET", "/establishments");
            this.establishments = response;
        },

        async fetch(method, url, headers = {}, body = null) {
            const response = await fetch(`/api${url}`, {
                method: method,
                headers: headers,
                body: body == null ? null : JSON.stringify(body)
            });

            if (!response.ok) {
                console.error("Failed to fetch resource", method, url, headers, body);
                return;
            }

            if (response.status == 204) {
                return null;
            }

            return await response.json();
        },

        openLoginWindow(url, client_id, width = 500, height = 700) {
            const parameters = new URLSearchParams({
                "url": url,
                "client_id": client_id,
                "redirect_uri": `${location.protocol}//${location.host}`
            })

            window.open(`/auth?${parameters.toString()}`, "auth", `popup,width=${width},height=${height}`);
        },

        loginMicrosoft() {
            this.openLoginWindow(
                "https://login.microsoftonline.com/common/oauth2/v2.0/authorize", 
                "b600e93e-c5f6-44d3-b95f-948abfb15b80"
            );
        },

        loginGoogle() {
            this.openLoginWindow(
                "https://accounts.google.com/o/oauth2/v2/auth", 
                "463687060136-g6v6qjf7r1jh49lfpeogq3qm5rj7islk.apps.googleusercontent.com"
            );
        },

        async startSession(idToken) {
            if (idToken == null) {
                return;
            }

            const response = await this.fetch(
                "POST", "/user/session", 
                { "Content-Type": "application/json" }, 
                { "id_token": idToken }
            );

            this.session = response.token;
            await this.fetchProfile();
        },

        async fetchProfile() {
            if (this.session == null) {
                return;
            }
            
            const response = await this.fetch(
                "GET", "/user/profile", 
                { "Authorization": `Bearer ${this.session}` }
            );

            this.user = response;
        },

        async logout() {
            if (this.session == null) {
                return;
            }

            const response = await this.fetch(
                "DELETE", "/user/session", 
                { "Authorization": `Bearer ${this.session}` }
            );

            this.session = null;
            this.user = null;
        },

        async vote(date, establishment, item) {
            if (this.session == null) {
                return;
            }

            await this.fetch(
                "PUT", "/vote", 
                { "Authorization": `Bearer ${this.session}`, "Content-Type": "application/json" },
                { "date": date, "establishment": establishment, "item": item }
            );
        }
    }));

    Alpine.data("menu", (establishment = null, linkOnly = false) => ({
        menu: null,

        async init() {
            if (!linkOnly) {
                const response = await this.fetch(
                    "GET", `/establishments/${establishment}`
                );

                this.menu = response;
            } else {
                this.menu = {
                    "week": [
                        {
                            "name": "(Hlasovat)"
                        }
                    ]
                };
            }
        }
    }));
});

window.Alpine = Alpine;

Alpine.plugin(persist);
Alpine.start();