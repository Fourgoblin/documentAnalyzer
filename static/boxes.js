let sectionStorage = {};
let allSections = []; //these are used for sharing info regarding each content section across functions as needed


function deleteAllBoxes() { //function to delete all boxes, runs just before new boxes are created following image scan
  let boxes = document.getElementsByClassName("resizable");
  while (boxes.length > 0) {
    while(boxes[0].hasChildNodes()) {
      boxes[0].removeChild(boxes[0].firstChild);
    }
    boxes[0].parentNode.removeChild(boxes[0]);
  }
  allSections = [];

}


function storeAllSectionsData(sections) { //function used to get data of all sections, used during JSON save process
 var sectionsArray = [];

  sections.forEach(section => {
    let sectionObject = { 
        section_id: section.section_id,
        top_left_x: section.top_left_x,
        top_left_y: section.top_left_y,
        width: section.width,
        height: section.height

    };

    sectionsArray.push(sectionObject);
  });
  return(sectionsArray);
}



function saveJson() { //function to save any changes made to JSON generated from image scanner, collects data from all current resizable sections
    var document_sections = [];
    const resizables = document.getElementsByClassName("resizable");
    const resizeArray = Array.from(resizables);
    resizeArray.forEach(resizable => {
      var data = {"section_id": resizable.id, "top_left_x": resizable.style.left, "top_left_y": resizable.style.top, "width": resizable.style.width, height:resizable.style.height};
      document_sections.push(data)
    });


    fetch('/save-json', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(document_sections)
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Error:', error));

    textObj.textContent = "JSON Saved";
}


function makeResizableDiv(div) { //function allowing for creation of resizable boxes, called whenever a new box must be made
  const elements = document.querySelectorAll(div); 
  elements.forEach(element => {
    
  
  const resizers = element.querySelectorAll(div + ' .resizer')
  const minimum_size = 20;
  let original_width = 0;
  let original_height = 0;
  let original_x = 0;
  let original_y = 0;
  let original_mouse_x = 0;
  let original_mouse_y = 0;

   resizers.forEach(resizer => {
    const currentResizer = resizer;
    currentResizer.addEventListener('mousedown', function(e) {
      e.preventDefault()
      original_width = parseFloat(getComputedStyle(element, null).getPropertyValue('width').replace('px', ''));
      original_height = parseFloat(getComputedStyle(element, null).getPropertyValue('height').replace('px', ''));
      parent_left = document.getElementById('image_holder').getBoundingClientRect().left;
      original_x = element.getBoundingClientRect().left;
      original_x = parent_left - original_x; //alter value to be relative to div rather than full page
      parent_top = document.getElementById('image_holder').getBoundingClientRect().top;
      original_y = element.getBoundingClientRect().top;
      original_y = parent_top - original_y; 
      original_mouse_x = e.pageX;
      original_mouse_y = e.pageY;
      window.addEventListener('mousemove', resize)
      window.addEventListener('mouseup', stopResize)
    })
  
    
    function resize(e) { //allows for actual resizing logic for each content box
      if (currentResizer.classList.contains('bottom-right')) {
        const width = original_width + (e.pageX - original_mouse_x);
        const height = original_height + (e.pageY - original_mouse_y)
        if (width > minimum_size) {
          element.style.width = width + 'px'
        }
        if (height > minimum_size) {
          element.style.height = height + 'px'
        }
      }
      else if (currentResizer.classList.contains('bottom-left')) {
        const height = original_height + (e.pageY - original_mouse_y)
        const width = original_width - (e.pageX - original_mouse_x)
        if (height > minimum_size) {
          element.style.height = height + 'px'
        }
        if (width > minimum_size) {
          element.style.width = width + 'px'
          element.style.left = (-1*original_x) + (e.pageX - original_mouse_x) + 'px' //Subtracting by original_x to account for location of div within page, same for other corners and height
        }
      }
      else if (currentResizer.classList.contains('top-right')) {
        const width = original_width + (e.pageX - original_mouse_x)
        const height = original_height - (e.pageY - original_mouse_y)
        if (width > minimum_size) {
          element.style.width = width + 'px'
        }
        if (height > minimum_size) {
          element.style.height = height + 'px'
          element.style.top = (-1*original_y) + (e.pageY - original_mouse_y) + 'px'
        }
      }
      else {
        const width = original_width - (e.pageX - original_mouse_x)
        const height = original_height - (e.pageY - original_mouse_y)
        if (width > minimum_size) {
          element.style.width = width + 'px'
          element.style.left = (-1*original_x) + (e.pageX - original_mouse_x) + 'px'
        }
        if (height > minimum_size) {
          element.style.height = height + 'px'
          element.style.top = (-1*original_y) + (e.pageY - original_mouse_y) + 'px'
        }
      }
    }
    
    function stopResize() {
      window.removeEventListener('mousemove', resize)
    }
  });
});
}

function createResizeHTML() { //allows for creation of singular resizable box as needed, number of box will be lowest number not currently in use starting at 1

  var resizeList = document.getElementsByClassName("resizable"); //get current number of boxes
  var checkName = "";
  var idList = [];
  var missingList = [];
  var i = 1;
  var missingNum = 0;
  for(let resizable of resizeList) { //goes through all boxes to see which section #s are missing so they can be assigned later
    idList.push(resizable.id);
  }
  for (i; i <= idList.length; i += 1) {
    if (idList.includes("section_"+i.toString())) {

    }
    else {
      missingList.push(i);
    }

   
    
    
  }

  if (missingList.length === 0) {
    missingNum = idList.length + 1;
  }
  else {
    missingNum = missingList[0];
  }
    
    
  

  
  checkName = "section_" + missingNum.toString();
  
  var div = document.createElement("div");
  div.setAttribute("class", "resizable");
  div.setAttribute('id', checkName);

  var resizers = document.createElement('div');
  resizers.setAttribute("class", "resizers");
  resizers.setAttribute('id', 'resizers'+missingNum.toString());

  var topLeft = document.createElement('div');
  topLeft.setAttribute('class', 'resizer top-left');
  var topRight = document.createElement('div');
  topRight.setAttribute('class', 'resizer top-right');
  var bottomLeft = document.createElement('div');
  bottomLeft.setAttribute('class', 'resizer bottom-left');
  var bottomRight = document.createElement('div');
  bottomRight.setAttribute('class', 'resizer bottom-right');

  div.style.left = '100px';
  div.style.top = '100px';
  div.style.width = '100px';
  div.style.height = '100px';

  document.getElementById("image_holder").appendChild(div);
  document.getElementById(checkName).appendChild(resizers); 
  document.getElementById("resizers"+missingNum.toString()).appendChild(topLeft);
  document.getElementById("resizers"+missingNum.toString()).appendChild(topRight);
  document.getElementById("resizers"+missingNum.toString()).appendChild(bottomLeft);
  document.getElementById("resizers"+missingNum.toString()).appendChild(bottomRight);

  makeResizableDiv('.resizable')
}

let lastClickedParent = null; //used for tracking of which resizable div has been clicked last so it may be deleted, both parent and child must be tracked to ensure selection is correct and visualized
let lastClickedChild = null;

document.addEventListener('click', function(event) { //event listener for if the user clicks on a resizable box, last clicked box changes to purple, others will remain blue
  const clickedElement = event.target;
  const clickedParent = clickedElement.parentElement;
  if (clickedParent.classList.contains('resizable')) {
    if (lastClickedChild) {
      lastClickedChild.style.border = "2px solid #4286f4" //sets child that had been selected before click back to blue
    }  
      
      lastClickedChild = clickedElement;
      lastClickedParent = clickedParent;
      clickedElement.style.border = "2px solid #6821bf" //sets most recent clicked to purple
  }
});


function deleteResizeHTML() { //allows for deletion of a single box by selecting the box that had been clicked last and removing it

  var childList = document.getElementById(lastClickedParent.id);
  while (childList.hasChildNodes()) {
    childList.removeChild(childList.firstChild)
  }
  childList.remove();

}


function createFromJson() { //function to generate boxes overlaying document based on result of image scanner
 
  fetch("static/"+newPath).then(function (response) { //fetch json file with corresponding name to image

    return response.json();
  
  }).then(data => {
  
    sectionStorage = data;
    allSections = storeAllSectionsData(sectionStorage.document_sections);

    var i = 1;
  allSections.forEach(section => {

  var div = document.createElement("div");
  div.setAttribute("class", "resizable");
  div.setAttribute('id', section.section_id);
  div.style.left = section.top_left_x+'px';
  div.style.top = section.top_left_y+'px';
  div.style.width = section.width+'px';
  div.style.height = section.height+'px';
  
  

  var resizers = document.createElement('div');
  resizers.setAttribute("class", "resizers");
  resizers.setAttribute('id', 'resizers' + i.toString());

  var topLeft = document.createElement('div');
  topLeft.setAttribute('class', 'resizer top-left');
  var topRight = document.createElement('div');
  topRight.setAttribute('class', 'resizer top-right');
  var bottomLeft = document.createElement('div');
  bottomLeft.setAttribute('class', 'resizer bottom-left');
  var bottomRight = document.createElement('div');
  bottomRight.setAttribute('class', 'resizer bottom-right');

  document.getElementById("image_holder").appendChild(div);
  document.getElementById(section.section_id).appendChild(resizers);
  document.getElementById("resizers"+i.toString()).appendChild(topLeft);
  document.getElementById("resizers"+i.toString()).appendChild(topRight);
  document.getElementById("resizers"+i.toString()).appendChild(bottomLeft);
  document.getElementById("resizers"+i.toString()).appendChild(bottomRight);

  i = i+1;

  });
  makeResizableDiv('.resizable');
  
  }).catch(function (error) {
    console.error("Something went wrong");
    console.error(error);
  })
  

  textObj.textContent = "Image Scanned";
  makeResizableDiv('.resizable');

}



