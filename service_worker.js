const CACHE_NAME = "king-diadem-cache-v1";

const urlsToCache = [
  "/",
  "/ask",
  "/system",
  "/dashboard"
];

// install
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

// fetch
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {

      if (response) {
        return response;
      }

      return fetch(event.request).then((networkResponse) => {

        return caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, networkResponse.clone());
          return networkResponse;
        });

      });

    })
  );
});

// activate
self.addEventListener("activate", (event) => {

  const cacheWhitelist = [CACHE_NAME];

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (!cacheWhitelist.includes(cacheName)) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );

});
