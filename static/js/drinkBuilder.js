document.addEventListener("DOMContentLoaded", () => {
    const drinkForm = document.getElementById("drink-form");
    const drinkOutput = document.getElementById("drink-output");

    drinkForm.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(drinkForm);
        fetch("/drinks", {
            method: "POST",
            body: formData,
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to create drink. Please ensure all fields are filled.");
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    drinkOutput.innerHTML = `<p class="error">${data.error}</p>`;
                } else {
                    drinkOutput.innerHTML = `
                        <h3>Your Custom Drink</h3>
                        <p><strong>Base Spirit:</strong> ${data["Base Spirit"]}</p>
                        <p><strong>Mixer:</strong> ${data["Mixer"]}</p>
                        <p><strong>Garnish:</strong> ${data["Garnish"]}</p>
                        <p>${data["Message"]}</p>
                    `;
                }
            })
            .catch(error => {
                drinkOutput.innerHTML = `<p class="error">${error.message}</p>`;
            });
    });
});

/* This JavaScript code dynamically handles the drink customization form submission,
    sends the data to a server endpoint, and displays a customized response or an error message.
    The implementation ensures that the user doesn't need to reload the page to see the results
    of their submission.
*/