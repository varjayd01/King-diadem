let chat_id = null;

async function init(){
  let res = await fetch("/new_chat",{method:"POST"});
  let data = await res.json();
  chat_id = data.chat_id;
}
init();

function addBubble(text,type){
  let div = document.createElement("div");
  div.className = "bubble "+type;
  div.innerText = text;
  document.getElementById("chat").appendChild(div);
  return div;
}

async function send(){
  let input = document.getElementById("input");
  let text = input.value;
  input.value="";

  addBubble(text,"user");
  let bubble = addBubble("...","ai");

  let res = await fetch("/ask_stream",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({chat_id,question:text})
  });

  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  let result = "";

  while(true){
    const {done,value} = await reader.read();
    if(done) break;

    result += decoder.decode(value);
    bubble.innerText = result;
  }
}
