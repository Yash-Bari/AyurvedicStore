// Example JavaScript code
document.addEventListener('DOMContentLoaded', function() {
    // Code to run when the DOM is fully loaded
    
    // Toggle navigation menu on small screens
    var menuButton = document.querySelector('#menu-button');
    var navMenu = document.querySelector('nav ul');
    
    if (menuButton && navMenu) {
        menuButton.addEventListener('click', function() {
            navMenu.classList.toggle('show');
        });
    }
});
