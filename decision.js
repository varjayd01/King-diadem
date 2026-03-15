async function analyze(){

const location=document.getElementById("location").value
const food=document.getElementById("food").value
const money=document.getElementById("money").value
const risk=document.getElementById("risk").value

const resultText=document.getElementById("resultText")

resultText.innerHTML="Analyzing strategic state..."

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
}
)

const data=await res.json()

resultText.innerHTML=

"<b>AI Strategic Output</b><br><br>"+
"Best Action: "+data.best_action+"<br>"+
"Score: "+data.score

}

catch(e){

resultText.innerHTML="System error. Node reconnecting..."

}

}

async function buyAccess(){

const res=await fetch(
"https://king-diadem.onrender.com/create-checkout",
{method:"POST"}
)

const data=await res.json()

window.location=data.url

}
