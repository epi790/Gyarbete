// Tack ChatGPT

var d;

// Set a unique session ID as a cookie

if (document.cookie.split('=')[0] == "sessionId") {

    
} else {
    setCookie('sessionId', generateSessionId(), 1); // Expires in 1 day
}


function changeImage(imageSrc, IsPub) {
    //alert("a")
    //d = new Date;


    document.getElementById('imageDisplay').src = imageSrc;

    // Remove the 'selected' class from all buttons
    const buttons = document.querySelectorAll('.button-container button');
    buttons.forEach(button => {
        button.classList.remove('selected');
    });

    // Find the button with the corresponding image path
    const activeButton = Array.from(buttons).find(button => button.getAttribute('data-image') === imageSrc);

    // Add the 'selected' class to the found button
    if (activeButton) {
        activeButton.classList.add('selected');
    }


    if (IsPub) {

    setTimeout(function(){
    //foo
},10000); //delay is in milliseconds 

    }

}

// Function to set a cookie
function setCookie(name, value, days) {
    const expires = new Date();
    expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
}

// Function to generate a unique session ID
function generateSessionId() {
    // Implement your own logic to generate a unique session IDgetT
    // You can use libraries like uuid or generate a random string
    // Example using Math.random():
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
}

function updateImages() {
    // Make an AJAX request to the Flask endpoint


    if (document.getElementsByClassName("button-container")[0].children[1].getAttribute("data-image") != document.getElementById("imageDisplay").src ) {

        // Parse cookies from document.cookie
        const cookies = document.cookie.split(';').map(cookie => cookie.trim());

        // Create a headers object with the cookies
        const headers = {
        'Cookie': cookies.join(';')
        };


        fetch('/create_image_datas_jsonified', {
            method: 'GET',
            headers: {
                'Cookie': document.cookie
            }})
        .then(response => response.json())
        .then(data => {
            // Update image elements with new data
            document.getElementById('imageDisplay').src = data.derived;
           
        })
        .catch(error => console.error('Error updating images:', error));
    }
    else {

        const cookies = document.cookie.split(';').map(cookie => cookie.trim());

        // Create a headers object with the cookies
        const headers = {
        'Cookie': cookies.join(';')
        };


        fetch('/create_image_datas_jsonified', {
            method: 'GET',
            headers: {
                'Cookie': document.cookie
            }})
        .then(response => response.json())
        .then(data => {
            // Update image elements with new data
            document.getElementById('imageDisplay').src = data.public;
            document.getElementsByClassName("button-container")[0].children[1].setAttribute("data-image", data.public)
           
        })
        .catch(error => console.error('Error updating images:', error));
    }

    
}

// Call updateImages initially and every 10 seconds thereafter
updateImages();
setInterval(updateImages, 500); // 1 seconds interval

		
// setInterval(function() {update();	}, 1000)

// 	function update() {
//     d = new Date;
//       document.getElementById('imageDisplay').src = document.getElementById('imageDisplay').src.split('?')[0] +  "?=" + d.getTime();

//   			}


