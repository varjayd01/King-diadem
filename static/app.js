async function ask(){
    let q = document.getElementById("q").value

    let res = await fetch("/ask", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({question:q})
    })

    let data = await res.json()

    document.getElementById("ans").innerText = data.answer
}

async function save(){
    let name = document.getElementById("name").value
    let tone = document.getElementById("tone").value

    await fetch("/save_profile", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({name, tone})
    })

    alert("Saved")
}

async function loadDash(){
    let res = await fetch("/dashboard")
    let data = await res.json()

    document.getElementById("dash").innerText =
        JSON.stringify(data, null, 2)
}

async function sendGroup(){
    let msg = document.getElementById("gmsg").value

    await fetch("/group_send", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({msg})
    })

    loadGroup()
}

async function loadGroup(){
    let res = await fetch("/group_get")
    let data = await res.json()

    let box = document.getElementById("groupBox")

    box.innerHTML = ""

    data.messages.forEach(m=>{
        let p = document.createElement("p")
        p.innerText = m
        box.appendChild(p)
    })
}

setInterval(loadGroup, 3000)
