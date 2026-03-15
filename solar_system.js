const canvas=document.getElementById("space")

const renderer=new THREE.WebGLRenderer({

canvas:canvas,
alpha:true

})

renderer.setSize(window.innerWidth,window.innerHeight)

const scene=new THREE.Scene()

const camera=new THREE.PerspectiveCamera(

60,
window.innerWidth/window.innerHeight,
0.1,
1000

)

camera.position.z=6

const light=new THREE.PointLight(0xffffff,2)

scene.add(light)

const loader=new THREE.TextureLoader()

const earthTexture=loader.load(

"https://threejsfundamentals.org/threejs/resources/images/earth-day.jpg"

)

const geo=new THREE.SphereGeometry(1.3,32,32)

const mat=new THREE.MeshStandardMaterial({

map:earthTexture

})

const earth=new THREE.Mesh(geo,mat)

scene.add(earth)

function animate(){

requestAnimationFrame(animate)

earth.rotation.y+=0.002

renderer.render(scene,camera)

}

animate()
