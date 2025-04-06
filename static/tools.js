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

function uploadImage() {
    const formData = new FormData(document.getElementById("uploadForm"));

    fetch("/UX", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.fileUrl) {
            const Image = document.getElementById("doc_image");
            Image.setAttribute("src", data.fileUrl.toString());
        }
    })
    .catch(error => console.error("Error:", error));
}