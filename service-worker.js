'use strict';

const CACHE_VERSION = 'qr-scanner-v1.1';
const APP_SHELL = [
    './',
    './index.html',
    './manifest.webmanifest',
    './icons/icon-192.png',
    './icons/icon-512.png',
    'https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_VERSION).then(function(cache) {
            return cache.addAll(APP_SHELL);
        }).then(function() {
            return self.skipWaiting();
        })
    );
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(keys) {
            return Promise.all(
                keys.filter(function(key) { return key !== CACHE_VERSION; })
                    .map(function(key) { return caches.delete(key); })
            );
        }).then(function() {
            return self.clients.claim();
        })
    );
});

// Никогда не кэшируем запросы к webhook — данные скана всегда должны идти в сеть
self.addEventListener('fetch', function(event) {
    const url = event.request.url;

    if (event.request.method !== 'GET') return;
    if (url.indexOf('/webhook/') !== -1) return;

    event.respondWith(
        caches.match(event.request).then(function(cached) {
            const network = fetch(event.request).then(function(response) {
                if (response && response.ok) {
                    const copy = response.clone();
                    caches.open(CACHE_VERSION).then(function(cache) {
                        cache.put(event.request, copy);
                    });
                }
                return response;
            }).catch(function() {
                return cached;
            });

            return cached || network;
        })
    );
});
