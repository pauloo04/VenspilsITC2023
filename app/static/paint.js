// Variables
let paint, size, alpha, clickX, clickY, priorX, priorY;

let paint_color = 0
// For undo/redo
let stateIndex = -1;
const states = [];

let redirect_url;
let redirect;

let canvasWidth, canvasHeight

// Saved image
var savedImage;
let img;

let eraser_toggled = false;

var socket = io.connect()
socket.emit("joinRoom", lobbyCode)

socket.on("redirect", function(url) {
  redirect_url = url["url"] + "?lobbyCode=" + lobbyCode + "&playerID=" + playerID
  window.location.href = redirect_url
})


window.onload = function() {
  socket.emit("getPrompt", lobbyCode, (prompt) => {
    document.getElementById("prompt").innerHTML = prompt
  })
  // Size
  document.getElementById('smlSize').addEventListener("click", function() {
    size = 2
  })
  document.getElementById('medSize').addEventListener("click", function() {
    size = 5
  })
  document.getElementById('bigSize').addEventListener("click", function() {
    size = 30
  })
  // Alpha
  document.getElementById('light').addEventListener("click", function() {
    alpha = 1
  })
  document.getElementById('medium').addEventListener("click", function() {
    alpha = 2
  })
  document.getElementById('dark').addEventListener("click", function() {
    alpha = 255
  })
  // Tools
  document.getElementById('undo').addEventListener("click", function() {
    undo();
  })
  document.getElementById('redo').addEventListener("click", function() {
    // Redo doesn't work for some reason, don't have a clue why
    // If you press y, redo works perfectly
    redo();
  })
  document.getElementById('delete').addEventListener("click", function() {
    clear()
    image(img, 0, 0)
  })
  document.getElementById('erase').addEventListener("click", function() {
    if (eraser_toggled) {
      eraser_toggled = false
      document.getElementById("erase").style.backgroundColor = "#7452ff"
      document.getElementById("erase").style.transition = "all 0.5s"
    }
    else {
      eraser_toggled = true
      document.getElementById("erase").style.backgroundColor = "#8e73fb"
      document.getElementById("erase").style.transition = "all 0.5s"
    }
  })
  document.getElementById("submitPainting").addEventListener("click", async function() {
    await new Promise(resolve => {
      document.getElementById("sketchArea").style.display = "none"
      document.getElementById("waitForOthers").style.display = "flex"
      socket.emit("painting", playerID, lobbyCode, canvas.toDataURL(), (redirectBool) => {
        redirect = redirectBool
        if (redirect==true){
          socket.emit("redirectToVote3", lobbyCode)
        }
        resolve(redirect)
      })
  })
})
}


// Create Canva
async function setup() {
  let canvasHeight = 600;
  let canvasWidth = 1.414213 * canvasHeight;
  // Set stroke weight
  size = 5;
  alpha = 255;  
  // Create Canva
  var canva = createCanvas(canvasWidth, canvasHeight);
  canva.parent("canvasHolder");
  canva.mouseReleased(function() {
    // If state has been undone, and now drawing something else
    // delete all of the states after the state where drawing now
    if (stateIndex < (states.length - 1)) {
      states.length = stateIndex + 1;
    }
    // If mouse hasn't moved since clicking it, don't record the state
    if (!(clickX == mouseX && clickY == mouseY)) {
      saveState();
    }
  })
  // Save coordinate when mouse is pressed
  canva.mousePressed(function() {  
    clickX = mouseX;
    clickY = mouseY;
  })
  // Set Canva background to white
  //background(color(255))
  await new Promise(resolve => {
    socket.emit("requestPNG", lobbyCode, playerID, "Painting", (images) => {
        img = loadImage(images, () => {
          img.resize(canvasWidth, canvasHeight)
          image(img, 0, 0)
        });
        resolve(img)
    })
  })
  colPic = createColorPicker("red");
  colPic.parent("colorPickerHolder");
  colPic.style("width", "8vw")
  colPic.style("height", "8vh")
  paint = colPic.color();
  frameRate(60);
  // noStroke();
  strokeJoin(ROUND);
};

// Runs continously at frame rate
function draw() {
  //store priorX and Y for line drawing
  priorX = mouseX;
  priorY = mouseY;
}

// If mouse is dragged draw a line
function mouseDragged() {
  if (eraser_toggled) {
    paint = color(255)
  }
  else {
    paint = colPic.color();
  }
  paint.setAlpha(alpha);
  color(paint)
  stroke(paint);
  strokeWeight(size);
  // Get mouse coordinates and add middle points
  // and middle between it
  mX = mouseX;
  mY = mouseY;
  midX = (priorX+mouseX)/2;
  midY = (priorY+mouseY)/2;
  mid1X = (priorX+midX)/2;
  mid1Y = (priorY+midY)/2;
  mid2X = (midX+mX)/2;
  mid2Y = (midY+mY)/2;
  line(priorX, priorY, mid1X, mid1Y);
  line(mid1X, mid1Y, midX, midY);
  line(midX, midY, mid2X, mid2Y);
  line(mid2X, mid2Y, mX, mY);
}

// Save current canva state
function saveState() {
  // Append state to array
  states.push(get());
  stateIndex += 1;
}

// When key pressed do Undo or Redo
function keyPressed(e) {
  // Undo (z)
  if (e.keyCode == 90) {
    undo();
  }
  // Redo (y)
  if (e.keyCode == 89) {
    redo();
  }
}

// Undo function
function undo() {
  // If no states saved, do nothing
  if (states.length == 0) {
    return;
  }
  // If undo past first saved state, show blank canva
  if (stateIndex < 0) {
    //background(color(255))
    //image(img, 0, 0, canvasWidth, canvasHeight)
    return;
  }
  // Index deincrement, because of undo
  stateIndex -= 1;
  // Set canva to blank
  background(color(255))
  image(img, 0, 0)
  // Load saved state using index
  if (stateIndex >= 0){
    image(states[stateIndex], 0, 0);
  }
}

// Redo function
function redo() {
  // If no states saved, do nothing
  if (states.length == 0) {
    return;
  }
  // Increment index to go to next saved state
  stateIndex += 1;
  // If index is last in saved states, do nothing
  if (stateIndex > states.length - 1) {
    stateIndex -= 1;
    return;
  }
  // Set canva to blank
  background(color(255))
  image(img, 0, 0)
  // Load saved state using index
  image(states[stateIndex], 0, 0);
}