document.getElementById('subscribe-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent page reload
    const formData = new FormData(this);
    const response = await fetch('/subscribe', {
        method: 'POST',
        body: formData,
    });
    const result = await response.json();
    const messageContainer = document.querySelector('.subscription-message');

    // Update the message text
    messageContainer.textContent = result.message;

    // Clear previous status classes
    messageContainer.classList.remove('success', 'error');

    // Add the appropriate class based on the status
    if (result.status === 'success') {
        messageContainer.classList.add('success');
    } else {
        messageContainer.classList.add('error');
    }
});

/*
    This JavaScript code handles the submission of a subscription form dynamically
    using the Fetch API. It prevents the default form submission behavior
    (which reloads the page), sends the form data to a server, and displays a
    success or error message based on the server's response.
*/