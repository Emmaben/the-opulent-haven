document.addEventListener('DOMContentLoaded', () => {
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach((question) => {
        question.addEventListener('click', () => {
            // Toggle the active class for the clicked question
            question.classList.toggle('active');

            // Toggle the display of the answer
            const answer = question.nextElementSibling;
            answer.style.display = answer.style.display === 'block' ? 'none' : 'block';
        });
    });
});

/*
    This JavaScript code enables an interactive FAQ (Frequently Asked Questions) functionality,
    where clicking on a question toggles its corresponding answer's visibility.
    It creates a simple accordion-style behavior, enhancing user experience by showing
    or hiding content dynamically.
*/