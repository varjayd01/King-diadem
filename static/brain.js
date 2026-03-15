async function loadBrain(){

const res = await fetch("/ai/brain");
const data = await res.json();

console.log("AI CORE:",data);

}

loadBrain();
