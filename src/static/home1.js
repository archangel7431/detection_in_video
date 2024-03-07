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

    document.getElementById("file-upload").addEventListener("change", function () {
        var formData = new FormData();
        formData.append("file", this.files[0]);

        fetch("/upload", {
            method: "POST",
            body: formData
        })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(error => console.error(error));
    });
};