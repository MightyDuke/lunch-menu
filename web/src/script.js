import Alpine from "/node_modules/alpinejs/dist/module.esm.js"
import persist from "/node_modules/@alpinejs/persist/dist/module.esm.js"
import sort from "/node_modules/@alpinejs/sort/dist/module.esm.js"

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

    for (const item of items) {
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
        user: undefined,
        layout: null,
        keywords: null,

        settingsOpen: false,

        async init() {
            this.selectedDate = getIsoDate(new Date);
            this.voteStream = new EventSource("/api/vote/stream");
            this.voteStream.onmessage = (event) => this.votes = { ...this.votes, ...JSON.parse(event.data) };

            window.sendIdToken = (idToken) => this.startSession(idToken);
            
            await this.fetchProfile();
            await this.fetchEstablishments();
        },

        async fetch(method, url, headers = {}, body = null) {
            const response = await fetch(`/api${url}`, {
                method: method,
                headers: headers,
                body: body == null ? null : JSON.stringify(body)
            });

            if (!response.ok) {
                throw new Error("Failed to fetch resource");
            }

            if (response.status == 204) {
                return null;
            }

            return await response.json();
        },

        openLoginWindow(url, client_id, width = 500, height = 600) {
            const parameters = new URLSearchParams({
                "client_id": client_id,
                "redirect_uri": `${location.protocol}//${location.host}/auth`,
                "response_type": "id_token", 
                "scope": "openid profile",
                "prompt": "select_account",
                "response_mode": "form_post",
                "nonce": window.crypto.randomUUID()
            })

            const x = window.screen.width / 2 - width / 2;
            const y = window.screen.height / 2 - height / 2;

            window.open(`${url}?${parameters.toString()}`, "oauth2LoginWindow", `popup,width=${width},height=${height},screenX=${x},screenY=${y}`);
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

        async fetchEstablishments() {
            const availableEstablishments = await this.fetch(
                "GET", "/establishments", 
            );

            if (this.session != null) {
                try {
                    const settings = await this.fetch(
                        "GET", "/user/settings",
                        { "Authorization": `Bearer ${this.session}` }
                    );

                    this.layout = settings.layout;
                    this.keywords = settings.keywords;
                } catch {
                    this.layout = null;
                    this.keywords = null;
                }
            } else {
                this.layout = null;
                this.keywords = null;
            }

            const establishments = Object.entries(availableEstablishments);
            
            for (let i = 0; i < establishments.length; i++) {
                const [key, establishment] = establishments[i];

                if (this.layout == null) {
                    establishment.enabled = true;
                    establishment.order = i;
                } else if (this.layout[key] == null) {
                    establishment.enabled = false;
                    establishment.order = i;
                } else {
                    Object.assign(establishment, this.layout[key]);
                }
                
                establishment.key = key;
                establishment.pendingEnabled = establishment.enabled;
            }

            this.establishments = establishments
                .map(x => x[1])
                .sort((a, b) => a.order > b.order ? 1 : a.order < b.order ? -1 : 0);
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
            await this.fetchEstablishments();
        },

        async fetchProfile() {
            if (this.session == null) {
                this.user = null;
                return;
            }
            
            try {
                const response = await this.fetch(
                    "GET", "/user/profile", 
                    { "Authorization": `Bearer ${this.session}` }
                );

                this.user = response;
            } catch {
                this.user = null;
            } 
        },

        async logout() {
            if (this.session == null) {
                return;
            }

            await this.fetch(
                "DELETE", "/user/session", 
                { "Authorization": `Bearer ${this.session}` }
            );

            this.session = null;
            this.user = null;
            this.layout = null;
            this.keywords = null;

            await this.fetchEstablishments();
        },

        async vote(date, establishment) {
            if (this.session == null) {
                return;
            }

            await this.fetch(
                "PUT", "/vote", 
                { "Authorization": `Bearer ${this.session}`, "Content-Type": "application/json" },
                { "date": date, "establishment": establishment }
            );
        },

        containsCurrentUserVote(selectedDate, establishment) {
            if (!(selectedDate in this.votes)) {
                return false;
            }
            
            if (!(establishment in this.votes[selectedDate])) {
                return false;
            }
            
            const ids = this.votes[selectedDate][establishment].map(x => x.id);
            
            if (ids.includes(this.user.id)) {
                return true;
            }

            return false;
        },

        containsKeyword(text) {
            if (this.keywords == null) {
                return false;
            }

            text = text.toLowerCase();

            for (const keyword of this.keywords) {
                if (text.includes(keyword.toLowerCase())) {
                    return true;
                }
            }

            return false;
        },

        reorderLayout(key, toIndex) {
            const oldEstablishment = this.establishments.find(x => x.order == toIndex);
            const newEstablishment = this.establishments.find(x => x.key == key);
            
            if (oldEstablishment == null || newEstablishment == null) {
                return;
            }

            oldEstablishment.order = newEstablishment.order;
            newEstablishment.order = toIndex;
        },

        async saveSettings(keywords) {
            if (this.session == null) {
                return;
            }

            let settings = {
                "keywords": [],
                "layout": {}
            };

            for (const establishment of this.establishments) {
                settings.layout[establishment.key] = { 
                    "enabled": establishment.pendingEnabled, 
                    "order": establishment.order 
                };
            }

            if (keywords != null && keywords != "") {
                keywords = keywords.trim();
                settings.keywords = keywords.split(",").map(x => x.trim());
            } else {
                settings.keywords = [];
            }

            await this.fetch(
                "PUT", "/user/settings",
                { "Authorization": `Bearer ${this.session}`, "Content-Type": "application/json" },
                settings
            );

            this.settingsOpen = false;
            await this.fetchEstablishments();
        },

        async deleteSettings() {
            if (this.session == null) {
                return;
            }

            const prompt = new Promise(resolve => {
                const result = window.confirm("Vrátit nastavení do výchozího stavu?");
                resolve(result);
            });

            const result = await prompt;

            if (!result) {
                return;
            }

            await this.fetch(
                "DELETE", "/user/settings",
                { "Authorization": `Bearer ${this.session}` }
            );

            this.settingsOpen = false;
            await this.fetchEstablishments();
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
                this.menu = {};
            }
        }
    }));
});

window.Alpine = Alpine;

Alpine.plugin(persist);
Alpine.plugin(sort);
Alpine.start();
