const backToTopButton = document.getElementById('back-to-top');

// Show the button when scrolling
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        backToTopButton.classList.add('show');
    } else {
        backToTopButton.classList.remove('show');
    }
});

// Scroll back to the top on click
backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

/*
    This JavaScript code implements a "Back to Top" button, which appears
    when the user scrolls down the page and provides a smooth scrolling effect when clicked.
*/