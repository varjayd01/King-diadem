const CACHE_NAME = "king-diadem-v1"

const urlsToCache = [

"/static/index.html",
"/static/style.css",
"/static/app.js",
"/static/system.js",
"/static/brain.js",
"/static/galaxy.js"

]

self.addEventListener("install",event=>{

event.waitUntil(

caches.open(CACHE_NAME)

.then(cache=>{

return cache.addAll(urlsToCache)

})

)

})

self.addEventListener("fetch",event=>{

event.respondWith(

caches.match(event.request)

.then(response=>{

return response || fetch(event.request)

})

)

})
