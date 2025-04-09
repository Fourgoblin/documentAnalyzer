var verticalSlider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = verticalSlider.value; // Display the default verticalSlider value

// Update the current verticalSlider value (each time you drag the verticalSlider handle)
verticalSlider.oninput = function() {
    output.innerHTML = this.value;
}

var horizontalSlider = document.getElementById("myRangeHorizontal");
var outputHorizontal = document.getElementById("demoHorizontal");
outputHorizontal.innerHTML = horizontalSlider.value;

horizontalSlider.oninput = function() {
    outputHorizontal.innerHTML = this.value;    

}
let newPath = ""
function uploadImage() {
    const file = document.getElementById('fileInput').files[0];
    const reader = new FileReader();
    newPath = modifyFileName(file.name);
    reader.onloadend = function() {
        const img = document.getElementById('doc_image');
        
        // Send the image data to Flask
        const formData = new FormData();
        formData.append('file', file);  // Send the actual file object, not just the base64 string
        img.src = reader.result;
        //img.src = "static/"+file.name;
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
        });
        
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


