async function loadSystemStatus(){

const res = await fetch("/system/health");
const data = await res.json();

console.log("SYSTEM STATUS:", data);

}

setInterval(loadSystemStatus,5000);

loadSystemStatus();
