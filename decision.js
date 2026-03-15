async function analyze(){

const location=document.getElementById("location").value
const food=document.getElementById("food").value
const money=document.getElementById("money").value
const risk=document.getElementById("risk").value


const resultBox=document.getElementById("resultBox")
const resultText=document.getElementById("resultText")


resultBox.style.display="block"

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
})

const data=await res.json()


let output="<b>AI Strategic Output</b><br><br>"

output+="Best Action: "+data.best_action+"<br>"

output+="Score: "+data.score+"<br>"


resultText.innerHTML=output


let prob=Math.min(
95,
Math.max(
10,
(Number(money)/10)+(food.length*5)-(risk.length*2)
)
)


document.getElementById("probBar").style.width=prob+"%"
document.getElementById("probText").innerHTML=prob+"%"


}catch(e){

resultText.innerHTML="System error. Node reconnecting..."

}

}
