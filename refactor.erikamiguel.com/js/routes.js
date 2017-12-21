/*
	This file describes the website routes using the Navigo library
*/

// Paraphrasing Navigo Demo here...
var root = null;
var useHash = false; // Defaults to: false
var hash = '#!'; // Defaults to: '#'
var router = new Navigo(root, useHash, hash);

// Creating Page Layouts
var welcome = new Page("welcome.html")
var notFound = new Page("notFound.html")
var home = new Layout(new Page("menu.html"), new Page("home.html"))
var blog = new Layout(new Page("menu.html"), new Page("blog.html"))
var about = new Page("blog.html");


async function loadHTML(layout, customElement) {
	await layout.load()
	var el = document.querySelector(customElement)
	el.innerHTML = ''
	layout.show(el)
 }

// Define routes i.e. erikamiguel.com/home, erikamiguel.com/blog, etc.
router.on({
  'home': () => { loadHTML(home, 'main') },
  'blog': () => { loadHTML(blog, 'main') },
  'about': () => { loadHTML(home, 'main'); loadHTML(about, 'homeData'); }
});

// Set main page
router.on(() => loadHTML(welcome, 'main'));

// Also paraphrasing Navigo Demo here...
router.notFound((query) => { loadHTML(notFound, 'main') });
router.resolve();