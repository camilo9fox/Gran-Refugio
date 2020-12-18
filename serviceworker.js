var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    'vet/inicio',
    '/static/css/materialize.min.css',
    '/static/js/materialize.min.js',
    '/static/css/estilo-base.css',
    '/static/js/script-base.js',
    '/static/imagenes/logo_vet.png',
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(

      fetch(event.request)
      .then((result)=>{
        return caches.open(CACHE_NAME)
        .then(function(c) {
          c.put(event.request.url, result.clone())
          return result;
        })
        
      })
      .catch(function(e){
          return caches.match(event.request)
      })
  

     
    );
});

