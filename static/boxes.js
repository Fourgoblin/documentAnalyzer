let testData = {};
let allSections = [];
//let sectionsArray = [];


function deleteAllBoxes() {
  let boxes = document.getElementsByClassName("resizable");
  while (boxes.length > 0) {
    while(boxes[0].hasChildNodes()) {
      boxes[0].removeChild(boxes[0].firstChild);
    }
    boxes[0].parentNode.removeChild(boxes[0]);
  }
  allSections = [];

}


function storeAllSectionsData(sections) {
  //allSections = [];
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



function saveJson() {
    var i = 0;
    var document_sections = [];
    const resizables = document.getElementsByClassName("resizable");
    const resizeArray = Array.from(resizables);
    resizeArray.forEach(resizable => {
      var data = {"section_id": resizable.id, "top_left_x": resizable.style.left, "top_left_y": resizable.style.top, "width": resizable.style.width, height:resizable.style.height};
      document_sections.push(data)
    });

    // Specify the file path (you can change the file name and path as needed)
    const filePath = 'static'+newPath;

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

    
}


function makeResizableDiv(div) {
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
      original_x = parent_left - original_x; //relative to parent (image holder) now
      parent_top = document.getElementById('image_holder').getBoundingClientRect().top;
      original_y = element.getBoundingClientRect().top;
      original_y = parent_top - original_y; //also now relative to the image holder to prevent div offset from messing with box location
      original_mouse_x = e.pageX;
      original_mouse_y = e.pageY;
      window.addEventListener('mousemove', resize)
      window.addEventListener('mouseup', stopResize)
    })
  
    
    function resize(e) {
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
          element.style.left = (-1*original_x) + (e.pageX - original_mouse_x) + 'px' //this needs to subtract according to where the left actually starts (working)
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

function createResizeHTML() { //bug arises of multiple boxes being created with the same ID only if the box numbers get out of order (i.e if 1 and 3 exist it will get stuck making 2s as it always breaks at 2)

  var resizeList = document.getElementsByClassName("resizable"); //get current number of boxes
  var i = 1;
  var checkName = "";
  for(let resizable of resizeList) {
    checkName = "section_" + i.toString();
    if (resizable.id !== checkName) {
      break;
    }
    else {
      i += 1;
    }
  };
  checkName = "section_" + i.toString();
  var resizeCount = resizeList.length + 1; //add 1 to account for the new box being created, issue may arise if one is deleted and then created as number may be off/reused
  var resizeCountStr = resizeCount.toString();

  var div = document.createElement("div");
  div.setAttribute("class", "resizable");
  div.setAttribute('id', checkName);

  var resizers = document.createElement('div');
  resizers.setAttribute("class", "resizers");
  resizers.setAttribute('id', 'resizers'+i.toString());

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
  document.getElementById("resizers"+i.toString()).appendChild(topLeft);
  document.getElementById("resizers"+i.toString()).appendChild(topRight);
  document.getElementById("resizers"+i.toString()).appendChild(bottomLeft);
  document.getElementById("resizers"+i.toString()).appendChild(bottomRight);

  makeResizableDiv('.resizable')
}

let lastClickedParent = null;
let lastClickedChild = null;

document.addEventListener('click', function(event) {
  const clickedElement = event.target;
  const clickedParent = clickedElement.parentElement;
  if (clickedParent.classList.contains('resizable')) {
    if (lastClickedChild) {
      lastClickedChild.style.border = "2px solid #4286f4"
    }  
      
      lastClickedChild = clickedElement;
      lastClickedParent = clickedParent;
      clickedElement.style.border = "2px solid #6821bf"
  }
});


function deleteResizeHTML() { //functions, but will need a way to choose which box to delete

  var childList = document.getElementById(lastClickedParent.id);
  while (childList.hasChildNodes()) {
    childList.removeChild(childList.firstChild)
  }
  childList.remove();

}


function createFromJson() {
 
  fetch("static/"+newPath).then(function (response) {

    return response.json();
  
  }).then(data => {
  
    testData = data;
    allSections = storeAllSectionsData(testData.document_sections);

    var i = 0;
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
  
  
  
  
  var i = 0;
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
}



