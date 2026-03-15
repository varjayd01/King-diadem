function thinkingAnimation(){

let dots = document.getElementById("thinking")

let i = 0

setInterval(()=>{

dots.innerText = ".".repeat(i%4)

i++

},400)

}
