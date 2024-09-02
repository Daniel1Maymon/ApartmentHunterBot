function setupEventListeners() {
    const form = document.getElementById("user-form")

    // Find the "Add +" button by its ID
    const addEmailBtn = document.getElementById("add-email-btn");

    // Listen for a click event on the button
    addEmailBtn.addEventListener("click", addEmailInput);

    console.log("form");
    console.log(form);

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        // Handle form submission logic here
        console.log("Form submitted");

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const link1 = document.getElementById("link1").value;
        const email1 = document.getElementById("email1").value;
    })
    
}

// Function to add a new email input field
function addEmailInput() {
    // Find the last email input to generate a new ID
    const lastEmailInput = document.querySelectorAll('input[name="addresses[]"]');
    const newId = `email${lastEmailInput.length + 1}`; // Generate a unique ID

    // Create a new input element with identical attributes
    const newInput = document.createElement("input");
    newInput.type = "text";
    newInput.name = "addresses[]";
    newInput.placeholder = "Email address for notification";
    newInput.id = newId; // Set the new unique ID
    // newInput.className = "email-input"; // You can add a CSS class if needed
    // newInput.style.marginTop = "10px"; // Add spacing between input fields

    // Append the new input field to the "email-addresses" div
    const emailGroup = document.getElementById("email-addresses");
    emailGroup.appendChild(newInput);
}

document.addEventListener("DOMContentLoaded", setupEventListeners)
