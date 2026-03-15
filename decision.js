async function analyze(){

const location=document.getElementById("location").value
const food=document.getElementById("food").value
const money=document.getElementById("money").value
const risk=document.getElementById("risk").value

document.getElementById("result").innerHTML="Analyzing..."

try{

const res=await fetch(

"https://king-diadem.onrender.com/decision",

{

method:"POST",

headers:{

"Content-Type":"application/json"

},

body:JSON.stringify({

location:location,
food:food,
money:money,
risk:risk

})

})

const data=await res.json()

document.getElementById("result").innerHTML=

"Best action: "+data.best_action

}catch{

document.getElementById("result").innerHTML=

"System reconnecting..."

}

}
