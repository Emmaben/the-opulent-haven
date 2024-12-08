document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".nav-link");
    const currentPath = window.location.pathname;

    // Set active class based on current path
    links.forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });
});

function setActive(event) {
    const links = document.querySelectorAll(".nav-link");

    // Remove active class from all links
    links.forEach(link => link.classList.remove("active"));

    // Add active class to the clicked link
    event.target.classList.add("active");
}

// Retain toggleMenu function
function toggleMenu() {
    const navigation = document.querySelector(".navigation");
    navigation.classList.toggle("open"); // Example: toggling a class
}

/*
    This code dynamically manages the "active" class for navigation links (.nav-link)
    based on the current URL path and user interactions.
    It ensures that:
        1. The link corresponding to the current page is highlighted as "active" when the page loads.
        2. Clicking on a navigation link updates the "active" state dynamically.
        3. The menu toggling functionality (toggleMenu) is preserved.
*/