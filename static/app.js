let currentUser = ""

async function reg(){
    const f = new FormData()
    f.append("username", r_user.value)
    f.append("password", r_pass.value)

    const res = await fetch("/register",{method:"POST",body:f})
    out.innerText = JSON.stringify(await res.json(),null,2)
}

async function login(){
    const f = new FormData()
    f.append("username", l_user.value)
    f.append("password", l_pass.value)

    const res = await fetch("/login",{method:"POST",body:f})
    const data = await res.json()

    if(data.status==="ok"){
        currentUser = l_user.value
    }

    out.innerText = JSON.stringify(data,null,2)
}

async function run(){
    const res = await fetch("/ENGINE",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            location:location.value,
            food:food.value,
            money:parseInt(money.value),
            risk:parseInt(risk.value),
            username:currentUser
        })
    })

    out.innerText = JSON.stringify(await res.json(),null,2)
}
