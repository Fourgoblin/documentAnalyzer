let textObj = document.getElementById("statusText")
var verticalSlider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = verticalSlider.value; // Display the default verticalSlider value

// Update the current verticalSlider value (each time you drag the verticalSlider handle)
verticalSlider.oninput = function() {
    output.innerHTML = this.value;
    scanImage();
}

var horizontalSlider = document.getElementById("myRangeHorizontal");
var outputHorizontal = document.getElementById("demoHorizontal");
outputHorizontal.innerHTML = horizontalSlider.value;

horizontalSlider.oninput = function() {
    outputHorizontal.innerHTML = this.value;    
    scanImage();
}

//verticalSlider.addEventListener('input', scanImage());
//horizontalSlider.addEventListener('input', scanImage());
let newPath = ""

function scanImage() {
    deleteAllBoxes();
    
    textObj.textContent = "Scanning Image";
    const file = document.getElementById('fileInput').files[0];
    const reader = new FileReader();
    newPath = modifyFileName(file.name);
    reader.onloadend = function() {
        const formData = new FormData();
        formData.append('file', file);  // Send the actual file object, not just the base64 string
        formData.append('slider1', document.getElementById("myRangeHorizontal").value);  // append slider1 value
        formData.append('slider2', document.getElementById("myRange").value);  // append slider2 value

        fetch('/Image_Scanner', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text())
        .then(result => {

            if (result === "Image Scanned Successfully") {
                createFromJson(newPath);
            }
            console.log(result);  // Handle the response from Flask if needed
        })
        .catch(error => {
            console.error('Error uploading image:', error);
            textObj.textContent = "Upload Error";
        });
    }
    if(file) {
        reader.readAsDataURL(file);
    }

}
function uploadImage() {
    
    
    const file = document.getElementById('fileInput').files[0];
    const reader = new FileReader();
    newPath = modifyFileName(file.name);
    reader.onloadend = function() {
        const img = document.getElementById('doc_image');
        
        // Send the image data to Flask
        
        img.src = reader.result;
        //img.src = "static/"+file.name;
        
        
    }

    if (file) {
        reader.readAsDataURL(file);  // Read the file as a data URL for the img preview
    } else {
        preview.innerHTML = 'No file selected';
    }

    
}


function modifyFileName(fileName) {
  // Remove the file extension using a regular expression
  return fileName.replace(/\.[^/.]+$/, '') + '_analyzed.json';
}


