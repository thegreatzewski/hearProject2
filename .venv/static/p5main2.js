var x, y, z;
var xpos, ypos;

function setup() 
{

  keyID = int(random(1000));
  console.log(keyID);

  // set canvas size
  createCanvas(displayWidth, displayHeight);
  frameRate(30)

  // default values
  xpos = displayWidth/2;
  ypos = displayHeight/2;
  x = 0;
  y = 0;
}

function draw() 
{
  // set background color to white
  background(247, 248, 190);

  // add/subract xpos and ypos
  xpos = xpos - x;
  ypos = ypos + y; 

  if(xpos > displayWidth) { xpos = 0; }
  if(xpos < 0) { xpos = displayWidth; }
  if(ypos > displayHeight) { ypos = 0; }
  if(ypos < 0) { ypos = displayHeight; }



  // draw ellipse
  fill(255);
  ellipse(xpos, ypos, 100, 100);

  // display variables
  fill(0);
  noStroke();
  text("x: " + x, 25, 25);
  text("y: " + y, 25, 50);
  text("z: " + z, 25, 75); 

    d = {
        "volume": y,
        "keyID": keyID,
    }

    $.get("/publish", data=d, crossdomain=false)


}

// accelerometer Data
window.addEventListener('devicemotion', function(e) 
{
  // get accelerometer values
  x = parseInt(e.accelerationIncludingGravity.x);
  y = parseInt(e.accelerationIncludingGravity.y);
  z = parseInt(e.accelerationIncludingGravity.z); 


  
});