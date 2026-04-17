async function run(){

    const data = {
        entropy: Number(document.getElementById("entropy").value) || 40,
        resource: Number(document.getElementById("resource").value) || 50,
        stability: Number(document.getElementById("stability").value) || 60
    }

    const out = document.getElementById("out")
    out.innerText = "Processing..."

    try{
        const r = await fetch("/ENGINE",{
            method:"POST",
            headers:{ "Content-Type":"application/json"},
            body: JSON.stringify(data)
        })

        if(!r.ok){
            throw new Error("Server error " + r.status)
        }

        const d = await r.json()

        if(d.status === "HALT"){
            out.innerText = "⚠️ SYSTEM HALTED\n" + JSON.stringify(d,null,2)
            return
        }

        out.innerText = JSON.stringify(d,null,2)

    }catch(e){
        out.innerText = "ERROR: " + e.message
    }
}
