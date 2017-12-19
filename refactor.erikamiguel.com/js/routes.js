/*
	This file describes the website routes using the Navigo library
*/

// Paraphrasing Navigo Demo here...
var root = null;
var useHash = false; // Defaults to: false
var hash = '#!'; // Defaults to: '#'
var router = new Navigo(root, useHash, hash);

function loadHTML(url, customElement) {
  $.get(url).then(res => document.querySelector('main').innerHTML = res )
}

router.on({
  'home': () => { loadHTML('views/menu.html') },
  'about': () => { loadHTML('views/about.html') }
});

// Set main page
router.on(() => loadHTML('views/welcome.html'));

// Also paraphrasing Navigo Demo here...
router.notFound((query) => { loadHTML('views/notFound.html') });

router.resolve();