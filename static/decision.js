async function ask(){

let text = prompt("Your problem")

if(!text) return

let r = await fetch("/decision",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
problem:text
})

})

let d = await r.json()

alert(JSON.stringify(d,null,2))

}
