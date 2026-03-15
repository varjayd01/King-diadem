const ctxChart=document.getElementById("simChart")

const simChart=new Chart(ctxChart,{

type:"line",

data:{

labels:["1","2","3","4","5","6","7","8"],

datasets:[{

label:"Decision Stability",

data:[10,18,9,22,16,12,25,30],

borderColor:"#4fd1ff"

}]

},

options:{

responsive:true

}

})
