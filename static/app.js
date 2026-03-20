let chat_id = null;

async function init(){
  let res = await fetch("/new_chat",{method:"POST"});
  let data = await res.json();
  chat_id = data.chat_id;
}
init();

async function send(){
  let input = document.getElementById("input");
  let text = input.value;
  input.value="";

  addBubble(text,"user");

  let res = await fetch("/ask",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({chat_id,question:text})
  });

  let data = await res.json();
  addBubble(data.answer,"ai");
}

function addBubble(text,type){
  let div = document.createElement("div");
  div.className = "bubble "+type;
  div.innerText = text;

  let time = document.createElement("div");
  time.className = "time";
  time.innerText = new Date().toLocaleTimeString();
  div.appendChild(time);

  div.onmousedown = ()=> time.style.display="block";
  div.onmouseup = ()=> time.style.display="none";

  document.getElementById("chat").appendChild(div);
}
