async function ask(){

let q=document.getElementById("q").value

let res=await fetch("/ask",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({question:q})
})

let data=await res.json()

document.getElementById("res").innerText=data.answer
}

// NOTE SYSTEM
function process(){

let t=document.getElementById("note").value

let arr=t.split(/,|\n|และ/)
arr=arr.filter(x=>x.length>3)

let html=""

arr.forEach(x=>{
html+=`<p><input type="checkbox"> ${x}</p>`
})

html+=`<p>🎯 ทำอย่างน้อย ${Math.ceil(arr.length*0.6)}</p>`

document.getElementById("out").innerHTML=html
}

// SAVE PROFILE
async function save(){

let name=document.getElementById("name").value
let style=document.getElementById("style").value

await fetch("/save_profile",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({name,style})
})

alert("saved")
}

// GAME
let board=[1,2,3,4,5,6,7,8,9]

function startGame(){
let html=""
board.forEach(n=>{
html+=`<button onclick="play(${n})">${n}</button>`
})
document.getElementById("game").innerHTML=html
}

function play(n){

if(n==6){
alert("⚠️ ห้ามลงเลข 6")
return
}

if(n==5){
alert("เกมนี้ไม่มีผู้ชนะนะคะ 🤍")
return
}

alert("เดินได้ค่ะ")
}
