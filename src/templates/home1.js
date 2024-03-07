// Hovering over the dropdown button will display the dropdown content. Also clicking on the 
// dropdown button will display the dropdown content. Clicking on the dropdown button again will
// hide the dropdown content. 


// NOTE $$$$$$$$$
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
};



