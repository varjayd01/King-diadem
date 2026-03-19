async function ask(){
    let q = document.getElementById("q").value

    let r = await fetch("/ask", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({question:q})
    })

    let d = await r.json()
    document.getElementById("ans").innerText = d.answer
}

async function save(){
    let name = document.getElementById("name").value
    let tone = document.getElementById("tone").value

    await fetch("/save_profile", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({name, tone})
    })

    alert("saved")
}

async function send(){
    let msg = document.getElementById("g").value

    await fetch("/group_send", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({msg})
    })

    load()
}

async function load(){
    let r = await fetch("/group_get")
    let d = await r.json()

    let box = document.getElementById("chat")
    box.innerHTML = ""

    d.messages.forEach(m=>{
        let p = document.createElement("p")

        if(m.emotion=="crisis") p.style.color="red"
        if(m.emotion=="low") p.style.color="orange"

        p.innerText = m.msg
        box.appendChild(p)
    })
}

setInterval(load, 3000)

async function dash(){
    let r = await fetch("/dashboard")
    let d = await r.json()

    document.getElementById("dash").innerText =
        JSON.stringify(d, null, 2)
}
