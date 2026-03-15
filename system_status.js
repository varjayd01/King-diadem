async function ping(){

try{

await fetch("https://king-diadem.onrender.com/health")

}

catch(e){

console.log("server sleeping")

}

}

setInterval(ping,30000)
