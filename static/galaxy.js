async function loadGalaxy(){

const res = await fetch("/ai/galaxy");
const data = await res.json();

console.log("GALAXY:",data);

}

loadGalaxy();
