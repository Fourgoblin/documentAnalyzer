let textObj = document.getElementById("statusText");
var verticalSlider = document.getElementById("sliderVert");
var verticalOutput = document.getElementById("valueVertical");
verticalOutput.innerHTML = verticalSlider.value; // Display the default verticalSlider value

// Update the current verticalSlider value (each time you drag the verticalSlider handle)
verticalSlider.oninput = function() {
    verticalOutput.innerHTML = this.value;
    scanImage(); //call image scanner when input of slider is changed
}

var horizontalSlider = document.getElementById("sliderHorizontal");
var outputHorizontal = document.getElementById("valueHorizontal");
outputHorizontal.innerHTML = horizontalSlider.value;

horizontalSlider.oninput = function() {
    outputHorizontal.innerHTML = this.value;    
    scanImage();
}


let newPath = "" //declared here to file name can be shared where needed

function scanImage() { //function to send data to flask server and call image scanner script
    deleteAllBoxes();
    
    textObj.textContent = "Scanning Image";
    const file = document.getElementById('fileInput').files[0];
    const reader = new FileReader();
    newPath = modifyFileName(file.name);
    reader.onloadend = function() {
        const formData = new FormData();
        formData.append('file', file);  // Send the actual file object, not just the base64 string
        formData.append('slider1', document.getElementById("sliderHorizontal").value);  // append slider1 value
        formData.append('slider2', document.getElementById("sliderVert").value);  // append slider2 value

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
        
        
    }

    if (file) {
        reader.readAsDataURL(file);  // Read the file as a data URL for the img preview
    } else {
        preview.innerHTML = 'No file selected';
    }

    
}


function modifyFileName(fileName) { //function used to remove existing file extension from given file and add needed text to end for use in creating boxes from JSON
  return fileName.replace(/\.[^/.]+$/, '') + '_analyzed.json';
}


