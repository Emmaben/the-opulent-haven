document.addEventListener("DOMContentLoaded", function () {
    const welcomeText = document.querySelector('.welcome-text');
    const menuSpeechContent = document.querySelector('.menu-speech-content');

    // Check if Intersection Observer is supported
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            threshold: 0.2 // Trigger when 20% of the element is visible
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-up-in');
                    observer.unobserve(entry.target); // Stop observing after animation
                }
            });
        }, observerOptions);

        // Observe elements only if they exist
        if (welcomeText) observer.observe(welcomeText);
        if (menuSpeechContent) observer.observe(menuSpeechContent);
    } else {
        // Fallback for browsers that don't support Intersection Observer
        if (welcomeText) welcomeText.classList.add('fade-up-in');
        if (menuSpeechContent) menuSpeechContent.classList.add('fade-up-in');
    }
});

/*
    This JavaScript code uses the Intersection Observer API to create a smooth,
    on-scroll animation effect for specific elements (.welcome-text and .menu-speech-content).
    When these elements come into view (e.g., the user scrolls down),
    they are animated with the addition of a CSS class (fade-up-in).
    The code includes a fallback for browsers that do not support the Intersection Observer API.
*/