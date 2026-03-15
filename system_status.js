async function checkSystem(){

try{

const res=await fetch(

"https://king-diadem.onrender.com/system"

)

const data=await res.json()

document.getElementById("system").innerHTML=

"System online"

}catch{

document.getElementById("system").innerHTML=

"Server reconnecting..."

}

}

checkSystem()

setInterval(checkSystem,10000)
