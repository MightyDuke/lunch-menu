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

window.chain = (...items) => {
    let result = [];

    for (let item of items) {
        if (item !== undefined) {
            result.push(...item);
        }
    }

    return result;
}

window.identity = (value) => value;

document.addEventListener("alpine:init", () => {
    Alpine.data("app", () => ({
        selectedDate: null,
        establishments: [],
        session: Alpine.$persist(null).as("session"),
        user: null,
        menuOpen: false,
        votes: {},

        async init() {
            google.accounts.id.initialize({
                client_id: "463687060136-g6v6qjf7r1jh49lfpeogq3qm5rj7islk.apps.googleusercontent.com",
                callback: async response => await this.startSession(response.credential)
            });

            google.accounts.id.renderButton(
                document.getElementById("google-login"),
                { 
                    locale: "cs",
                    theme: "filled_blue",
                    text: "signin_with",
                    size: "medium"
                }
            );

            this.selectedDate = isoDate(new Date);

            const response = await fetch("/api/establishments");
            this.establishments = await response.json();

            this.voteStream = new EventSource("/api/vote/stream");
            this.voteStream.onmessage = (event) => this.votes = { ...this.votes, ...JSON.parse(event.data) };

            if (this.session != null) {
                try {
                    await this.fetchProfile();
                } catch {
                    this.user = null;
                }
            }
        },

        async loginMicrosoft() {
            const msalConfig = {
                auth: {
                    clientId: "b600e93e-c5f6-44d3-b95f-948abfb15b80"
                },
                cache: {
                    cacheLocation: "sessionStorage",
                    storeAuthStateInCookie: false
                }
            };

            const instance = new msal.PublicClientApplication(msalConfig); 
            const request = {scopes: ["openid", "profile"]};

            const response = await instance.loginPopup(request);
            await this.startSession(response.idToken);
        },

        async loginGoogle() {
            document.querySelector('#google-login div[role=button]').click();
        },

        async startSession(idToken) {
            let response = await fetch("/api/user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "id_token": idToken
                })
            });

            if (response.status !== 200) {
                throw new Error();
            }

            response = await response.json();
            this.session = response.token;

            await this.fetchProfile();
        },

        async fetchProfile() {
            let response = await fetch("/api/user", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${this.session}`
                }
            });

            if (response.status !== 200) {
                throw new Error();
            }

            response = await response.json();
            this.user = response;
        },

        async logout() {
            let response = await fetch("/api/user", {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${this.session}`
                }
            });

            this.session = null;
            this.user = null;
        },

        async vote(date, path) {
            if (this.session == null) {
                return;
            }

            let response = await fetch("/api/vote", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${this.session}`
                },
                body: JSON.stringify({
                    "date": date,
                    "path": path
                })
            });
        }
    }));

    Alpine.data("menu", (establishment = null, linkOnly = false) => ({
        menu: null,

        async init() {
            if (!linkOnly) {
                const response = await fetch(`/api/establishments/${establishment}`);
                this.menu = await response.json();
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