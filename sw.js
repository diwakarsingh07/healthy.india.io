// Service Worker for PWA
const CACHE_NAME = 'healthy-india-v1';
const urlsToCache = [
  '/',
  '/auth.html',
  '/advanced_frontend.html',
  '/WhatsApp Image 2025-09-16 at 9.36.53 PM.jpeg',
  '/manifest.json'
];

// Install event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Fetch event
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});