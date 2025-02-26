

function checkLogin() {
    //busca o token no local storage
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/login";
        console.log("SEM TOKEN")
        return;
    }
    console.log("ACHEI O TOKEN")
    //validar o token
    fetch("http://localhost:8080/api/v1/auth/me", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error("erro na autenticação");
        };
        return response.json();
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error("Erro de autenticação:", error);
        window.location.href = "/login";
    });

}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "/login"
}