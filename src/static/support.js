// function to appear dropdown menu when we click on Upload File//
document.querySelector('.dropbtn').addEventListener('click', function () {
    var dropdownContent = document.querySelector('.dropdown-content');
    var computedStyle = window.getComputedStyle(dropdownContent);
    if (computedStyle.getPropertyValue('display') === 'none') {
        dropdownContent.style.display = 'block';
    } else {
        dropdownContent.style.display = 'none';
    }
});

//function for browsing file when we click on from device//
document.querySelector('.from-device-option').addEventListener('click', function () {
    // Show a dialogue box to ask for ROI inclusion
    var includeROI = confirm("Do you want to include a Region of Interest (ROI)?");
    if (includeROI) {
        // Code for when ROI is included
        console.log("ROI included");
    } else {
        // Code for when ROI is excluded
        console.log("ROI not included");
    }
    var fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.addEventListener('change', function (e) {
        var file = e.target.files[0];
        var filePath = URL.createObjectURL(file);
        console.log(filePath);
        // Create an object to hold the data
        window.data = {
            filePath: filePath
        };

    });
});

// Send the data to the server
fetch("http://localhost:5000/file", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(window.data)
})
    .then(function (response) {
        if (response.ok) {
            // Data successfully sent to the server
            console.log("File path sent to the server");
        } else {
            throw new Error("Error sending file path to the server");
        }
    })
    .catch(function (error) {
        console.log("Error:", error.message);
    });


//function to open webcam after clicking on use webcam//
document.querySelector('#webcamBtn').addEventListener('click', function () {
    // Show a dialogue box to ask for ROI inclusion
    var includeROI = confirm("Do you want to include a Region of Interest (ROI)?");
    if (includeROI) {
        // Code for when ROI is included
        console.log("ROI included");
    } else {
        // Code for when ROI is excluded
        console.log("ROI not included");
    }

    var newWindow = window.open('webcam.html', 'Webcam', 'width=800,height=600');
    if (newWindow) {
        newWindow.focus();
    } else {
        console.log('Failed to open the webcam window');
    }
});

// Fetching from server /data
fetch("http://localhost:5000/webcam")
    .then(function (response) {
        if (response.ok) {
            return response.json();
        }
        throw new Error("Network response was not ok.");
    })
    .then(function (data) {
        console.log(data);
        // Process the data received from the server
    })
    .catch(function (error) {
        console.log("Error:", error.message);
    });