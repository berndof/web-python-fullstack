import Alpine from 'alpinejs'
import collapse from '@alpinejs/collapse'
import focus from '@alpinejs/focus'
import mask from '@alpinejs/mask'
 
Alpine.plugin(mask)
Alpine.plugin(focus)
Alpine.plugin(collapse)
 
import { createIcons, icons, Sidebar } from 'lucide';
// Caution, this will import all the icons and bundle them.
createIcons({ icons });

Alpine.store('ui', {
    isSidebarOpen: true,
    toggleSidebar() {
        this.isSidebarOpen = !this.isSidebarOpen
    }
});

Alpine.store('auth', {
    user: null,
    error: '',
    
    async checkLogin() {
        if (!localStorage.getItem("token")) {
            window.location.href = "/login";
            return;
        }

        try {
            let response = await fetch('http://localhost:8080/api/v1/auth/me', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            });
            if (!response.ok) throw new Error('Not Authenticated'); // verificar o erro que a response retorna, se é usuário ou se é senha

            let data = await response.json();
            this.user = data;

        } catch (error) {
            window.location.href = "/login";
        }
    },

    async login(username, password) {
        const data = new URLSearchParams();
        data.append("grant_type", "password");
        data.append("username", username);
        data.append("password", password);
        data.append("client_id", "string"); //TODO ou o valor que sua API espera
        data.append("client_secret", "string"); // idem

        try {
            let response = await fetch('http://localhost:8080/api/v1/auth/token', {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: data
            });

            let result = await response.json();
            if (!response.ok) throw new Error(result.detail.message);
            localStorage.setItem("token", result.access_token);
            window.location.href = "/"

        } catch (error) {
            console.log(error)
            this.error = error;
        };
    },
    
    logout() {
        localStorage.removeItem("token");
        this.user = null;
        window.location.href = "/login"
    },
    
})


window.Alpine = Alpine
Alpine.start()

