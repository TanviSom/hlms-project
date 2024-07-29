const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.nav-menu');
const getStartedBtn = document.querySelector('#get-started-btn');
const signInBtn = document.querySelector('.nav-links-btn');
const overlay = document.querySelector('#overlay');
const closeBtn = document.querySelector('#close-btn');

menu.addEventListener('click', function() {
    menu.classList.toggle('is-active');
    menuLinks.classList.toggle('active');
})

getStartedBtn.addEventListener('click', function() {
    overlay.classList.add('active');
});

signInBtn.addEventListener('click', function() {
    overlay.classList.add('active');
});

closeBtn.addEventListener('click', function() {
    overlay.classList.remove('active');
});