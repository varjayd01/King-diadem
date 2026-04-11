let currentUser = ""

function show(msg){
    document.getElementById("out").innerText = msg
}

// REGISTER
async function reg(){
    const f = new FormData()
    f.append("username", r_user.value)
    f.append("password", r_pass.value)

    const res = await fetch('/register',{
        method:'POST',
        body:f
    })

    show(JSON.stringify(await res.json(),null,2))
}

// LOGIN
async function login(){
    const f = new FormData()
    f.append("username", l_user.value)
    f.append("password", l_pass.value)

    const res = await fetch('/login',{
        method:'POST',
        body:f
    })

    const data = await res.json()

    if(data.status === "ok"){
        currentUser = l_user.value
        show("✅ LOGIN SUCCESS")
    }else{
        show(JSON.stringify(data,null,2))
    }
}

// ENGINE
async function run(){

    if(!currentUser){
        show("❌ LOGIN ก่อน")
        return
    }

    const res = await fetch('/ENGINE',{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            location: location.value,
            food: food.value,
            money: parseInt(money.value || 0),
            risk: parseInt(risk.value || 0),
            username: currentUser
        })
    })

    show(JSON.stringify(await res.json(),null,2))
}
