document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('.reservation-form');

    if (form) { // Ensure the element exists
        form.addEventListener('submit', async function (e) {
            e.preventDefault(); // Prevent the default form submission

            const formData = new FormData(this);
            const response = await fetch('/contact', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            const messageContainer = document.querySelector('.reservation-message');

            if (messageContainer) {
                // Update the message content
                messageContainer.textContent = result.message;

                // Clear previous status classes
                messageContainer.classList.remove('success', 'error');

                // Add the appropriate status class
                if (result.status === 'success') {
                    messageContainer.classList.add('success');
                } else {
                    messageContainer.classList.add('error');
                }
            }
        });
    } else {
        console.error('The form with class "reservation-form" was not found.');
    }
});

/*
    This JavaScript code dynamically handles the submission of a reservation form
    (.reservation-form) using the Fetch API. It sends the form data to a server
    endpoint (/contact) without reloading the page and displays success or error
    messages based on the server's response.
*/