const ctx=document.getElementById("simChart")

new Chart(ctx,{

type:"line",

data:{

labels:["1","2","3","4","5","6","7","8"],

datasets:[{

label:"Decision Stability",

data:[10,18,9,22,15,11,25,30],

borderColor:"#4bd4ff",

backgroundColor:"rgba(75,212,255,0.2)"

}]

},

options:{responsive:true}

})
