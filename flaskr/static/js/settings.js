function setupEventListeners() {
    const form = document.getElementById("user-form")

    // Find the "Add +" button by its ID
    const addLinkBtn = document.getElementById("add-link-btn");

    // Listen for a click event on the button
    addLinkBtn.addEventListener("click", function(){
        addLinkInput(addLinkBtn); // Pass the button element to the function

    });

    console.log("form");
    console.log(form);

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        // Handle form submission logic here
        console.log("Form submitted");

        // const username = document.getElementById("username").value;
        // const password = document.getElementById("password").value;
        // const link1 = document.getElementById("link1").value;
        // const email1 = document.getElementById("email1").value;

        getAllLinkInputs()
    })
    
}

// Function to add a new email input field
function addLinkInput(addLinkBtn) {
    // Find the container where the new input should be added
    const linksContainer = document.querySelector('.links-input-field');

    // Get the current number of input elements in the container
    const currentInputs = linksContainer.querySelectorAll('input[name="links[]"]');


    // Check if the number of inputs is less than 5
    if (currentInputs.length < 5) {
        // Create a new input element
        const lastLinkInput = document.querySelectorAll('input[name="links[]"]');
        const newId = `link${lastLinkInput.length + 1}`; // Generate a unique ID for the new input

        const newInput = document.createElement("input");
        newInput.type = "text";
        newInput.name = "links[]";
        newInput.placeholder = "Enter a link";
        newInput.id = newId; // Set the new unique ID
        // newInput.className = "link-input"; // Add a CSS class if needed
        // newInput.style.marginTop = "10px"; // Add some space between the inputs

        // Insert the new input before the button
        linksContainer.insertBefore(newInput, addLinkBtn);
    }
    
}

function getAllLinkInputs() {
    // Find all input elements with name="links[]"
    const linkInputs = document.querySelectorAll('input[name="links[]"]');
    const linksArray = [];

    // Loop through each input and add its value to the array
    linkInputs.forEach(function (input) {
        if (input.value.trim() !== "") { // Only add non-empty inputs
            linksArray.push(input.value.trim());
        }
    });

    console.log("linksArray = " + linksArray);
    
    // return linksArray; // Return the array of links
}


document.addEventListener("DOMContentLoaded", setupEventListeners)
