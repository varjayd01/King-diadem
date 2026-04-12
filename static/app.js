// ===== REGISTER =====
async function register() {
    const u = document.getElementById("reg_user").value
    const p = document.getElementById("reg_pass").value

    const f = new FormData()
    f.append("username", u)
    f.append("password", p)

    const r = await fetch("/register", { method: "POST", body: f })
    const d = await r.json()

    alert(JSON.stringify(d))
}


// ===== LOGIN =====
async function login() {
    const u = document.getElementById("login_user").value
    const p = document.getElementById("login_pass").value

    const f = new FormData()
    f.append("username", u)
    f.append("password", p)

    const r = await fetch("/login", { method: "POST", body: f })
    const d = await r.json()

    if (d.status === "ok") {
        localStorage.setItem("user", u)
    }

    alert(JSON.stringify(d))
}


// ===== ENGINE =====
async function runEngine() {

    const username = localStorage.getItem("user")
    if (!username) {
        alert("login first")
        return
    }

    const data = {
        username,
        location: document.getElementById("location").value,
        food: document.getElementById("food").value,
        money: document.getElementById("money").value,
        risk: document.getElementById("risk").value
    }

    const r = await fetch("/ENGINE", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })

    const d = await r.json()

    console.log(d)

    alert(JSON.stringify(d, null, 2))
}
