// static/js/scripts.js

// Function to hide the button and show the loading spinner
function showLoading() {
    console.log("\n:: showLoading() ::\n");
    
    const runScraperBtn = document.getElementById("run-scraper-btn")
    const loadingSpinner = document.getElementById("loading-spinner")
    const loadingContent = document.getElementById("loading-content");

    runScraperBtn.style.display = 'none';
    loadingSpinner.style.display = 'block';
    loadingContent.style.display = "block";

    console.log("Spinner visibility:", window.getComputedStyle(loadingSpinner).display);  // Debugging line


}

// Function to show the button and hide the loading spinner
function hideLoading(){
    const runScraperBtn = document.getElementById("run-scraper-btn")
    const loadingSpinner = document.getElementById("loading-spinner")

    runScraperBtn.style.display = 'block';
    loadingSpinner.style.display = 'none'
    loadingContent.style.display = "none";
}

async function runScraper() {
    console.log(":: START runScraper ::");
    
    try {
        const response= await fetch('/run_scraper', {
            method: 'POST',
            headers: {
               'Content-Type': 'application/json' 
            }
        });

        const data = await response.json();
        alert(data.message);
    } catch (error) {
        alert("Error: " + error.message)
    }
    console.log(":: END runScraper ::");
    
}

// Function to handle the scraper execution process
async function handleRunScraper() {
    console.log("\nshowLoading()\n");
    
    showLoading();

    console.log("\nrunScraper()\n");
    await runScraper();

    console.log("\nhideLoading()\n");
    hideLoading()
}

// Function to set up event listeners
function setupEventListeners() {
    const runScraperBtn = document.getElementById('run-scraper-btn');
    console.log(runScraperBtn);

    if (runScraperBtn) {
        runScraperBtn.addEventListener('click', handleRunScraper)
    } else {
        console.error('Button with ID "run-scraper-btn" not found.');
    }


}

// document.getElementById('run-scraper-btn').addEventListener('click', runScraper)


document.addEventListener("DOMContentLoaded", setupEventListeners);
