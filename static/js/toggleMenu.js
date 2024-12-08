document.addEventListener('DOMContentLoaded', () => {
    function toggleMenu() {
        const menuToggle = document.querySelector('.menuToggle');
        const navigation = document.querySelector('.navigation');
        const header = document.querySelector("header");
        const body = document.body; // Select the body element

        if (menuToggle && navigation) {
            menuToggle.classList.toggle('active');
            navigation.classList.toggle('active');
            header.classList.toggle("menu-open");
            body.classList.toggle("no-scroll"); // Disable scrolling
        } else {
            console.error('Menu toggle or navigation element not found');
        }
    }

     // Close menu when clicking outside
    function closeMenuOnOutsideClick(event) {
        const navigation = document.querySelector('.navigation');
        const menuToggle = document.querySelector('.menuToggle');
        const header = document.querySelector("header");
        const body = document.body;

        if (navigation && !navigation.contains(event.target) && !menuToggle.contains(event.target)) {
            navigation.classList.remove('active');
            header.classList.remove("menu-open");
            menuToggle.classList.remove('active');
            body.classList.remove("no-scroll"); // Enable scrolling
        }
    }

    window.toggleMenu = toggleMenu; // Make the function accessible globally
    document.addEventListener('click', closeMenuOnOutsideClick); // Detect outside clicks
});


/*
    This JavaScript code provides functionality for a responsive menu toggle system.
    It ensures a menu can be opened and closed via a button and also closes the menu
    when the user clicks outside of it. Additionally, it disables scrolling while the menu is open.
*/