// Hovering over the dropdown button will display the dropdown content. Also clicking on the 
// dropdown button will display the dropdown content. Clicking on the dropdown button again will
// hide the dropdown content. 


// $$$$$$$ NOTE $$$$$$$$$
// need to make more flexible like other websites. but for now, this is enough.//
//

window.onload = function () {
    var dropdown = document.querySelector('.dropdown');
    var button = document.querySelector('.dropbtn');
    var dropdownContent = document.querySelector('.dropdown-content');

    button.onclick = function () {
        var isDisplayed = dropdownContent.style.display === 'block';
        dropdownContent.style.display = isDisplayed ? 'none' : 'block';
    };

    dropdown.onmouseleave = function () {
        dropdownContent.style.display = 'none';
    };


    // Event listener for file upload from device
    document.getElementById('upload-button').addEventListener('click', function (e) {
        e.preventDefault();
        document.getElementById('file-upload').click();
    });

    // Sending the video file via HTTP POST request
    document.getElementById("file-upload").addEventListener("change", function () {
        var file = this.files[0];

        // Validate file type
        var allowedTypes = ["video/mp4", "video/webm"]
        if (!allowedTypes.includes(file.type)) {
            document.getElementById('error-message').textContent = "Invalid file type. Only mp4 and webm files are allowed.";
            return;
        }

        // Validate file size
        var maxSizeInMB = 500;
        var maxSizeInBytes = maxSizeInMB * 1024 * 1024;
        if (file.size > maxSizeInBytes) {
            document.getElementById('error-message').textContent = "File size exceeds 5MB. Please upload a smaller file.";
            return;
        }

        var formData = new FormData();
        formData.append("file", this.files[0]);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error(error));

        // ROI: Yes or No?
        var roi = confirm("Do you want a ROI?");
        if (roi == true) {
            // User clicked OK, send a request to the server indicating that a ROI is wanted
            fetch('/set_roi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ roi: true }),
            })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch((error) => {
                    console.error('Error:', error);
                });
        } else {
            // User clicked Cancel, send a request to the server indicating that a ROI is not wanted
            fetch('/set_roi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ roi: false }),
            })
        }
    });



};