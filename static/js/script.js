const menuToggle = document.getElementById('menu-toggle');
const mobileNav = document.getElementById('mobile-nav');
const navBar = document.getElementById('header');


menuToggle.addEventListener('click', () => {
    mobileNav.classList.toggle('active');
    navBar.classList.toggle('mobile-active');
});