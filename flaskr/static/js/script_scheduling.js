
// Function to handle the OK button click
function handleOkButtonClick() {
    console.log("OK button clicked");
    
    // Collect values from the form
    const repeatInterval = document.getElementById('repeat-interval').value;
    const intervalUnit = document.getElementById('interval-unit').value;
    const startTime = document.getElementById('start-time').value;


    let endOption;
    let endDate = null;
    let occurrences = null;

    if (document.getElementById('never').checked) {
        endOption = 'never';
    } else if (document.getElementById('on-date').checked) {
        endOption = 'on-date';
        endDate = document.getElementById('end-date').value;
    } else if (document.getElementById('after-occurrences').checked) {
        endOption = 'after-occurrences';
        occurrences = document.getElementById('occurrences').value;
    }

    // Save the collected data
    const scheduleData = {
        repeatInterval: repeatInterval,
        intervalUnit: intervalUnit,
        startTime: startTime,
        endOption: endOption,
        endDate: endDate,
        occurrences: occurrences
    };

    // Log to the console for debugging
    console.log(scheduleData);

    // Call the function to save the data
    saveScheduleData(scheduleData);

} 

// Function to save the schedule data
function saveScheduleData(scheduleData){
    fetch(input='/save-schedule', url={
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(scheduleData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success: ', data);
        
    })
    .catch((error) => {
        console.log('Error:', error);
        
    });
}


document.getElementById('ok-btn').addEventListener('click', handleOkButtonClick);
