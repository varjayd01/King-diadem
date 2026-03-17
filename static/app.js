async function ask(){

let q=document.getElementById("question").value

let thinking=document.getElementById("thinking")
thinking.innerText="AI กำลังคิด..."

let res=await fetch("/ask",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({question:q})
})

let data=await res.json()

thinking.innerText=""

let box=document.getElementById("response")
box.style.opacity=0

box.innerText=data.answer

setTimeout(()=>{
box.style.opacity=1
},100)

// 🧭 แสดง compass จากข้อความ
extractCompass(data.answer)

}

// 🧭 ดึงทิศจาก response
function extractCompass(text){

let compassBox=document.getElementById("compassBox")

let match=text.match(/🧭(.+)/)

if(match){
compassBox.innerText=match[0]
}else{
compassBox.innerText=""
}

}

// 📿 QUOTE SYSTEM
let quotes=[
"นตฺถิ สติสมํ ปญฺญา\nไม่มีสิ่งใดสำคัญกว่าสติ\nNothing is more important than mindfulness",
"นตฺถิ ปญฺญาสมา อาภา\nไม่มีแสงใดสว่างเท่าปัญญา\nNo light shines brighter than wisdom"
]

function showQuote(){
let q=quotes[Math.floor(Math.random()*quotes.length)]
document.getElementById("quote").innerText=q
}

showQuote()
