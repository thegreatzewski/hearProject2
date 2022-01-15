var mic;
let keyID;
let r, g, b;
let rSlider;
//var socket = io();

function setup() {
    
//     //socket = io.connect('');
//     socket.on('volume',
//     // When we receive data
//     function(data) {
//       console.log("Got: " + data);
//     }
//   );

// $(document) .ready(function(){  
//     var socket = io.connect('http://' + document.domain + ':' + location.port)
//     $('form#emit').submit(function(event) {
//         socket.emit('volume', {data: $('#emit_data').val()});
//         return false;
//     })

// });

    keyID = int(random(1000));
    console.log(keyID);

    mic = new p5.AudioIn();
    mic.start();
    frameRate(10);
    createCanvas(displayWidth, displayHeight);
    // r = random(50, 255);
    // g = random(0, 200);
    // b = random(50, 255);
    textSize(200);

    rSlider = createSlider(0,300, 100);
    rSlider.position(300,300);

}
function draw() {


    background(r, g, b);
 
    
    var vol = mic.getLevel();
    // send vol to the server every frame. The framerate is 2 fps so this is every 500ms.
    // If you increrase the framerate, maybe you should use setTimeout instead
    
    
    
    textSize(16);
    fill(color('Green'));
    textAlign(CENTER);
    text("text", 600, 300);
    ellipse(100, 100, vol*1000, vol*1000);
    r = rSlider.value();
  

    console.log(vol);
    d = {
        "volume": vol,
        "keyID": keyID,
    }
    
    

    //socket.emit('volume', data )
    $.get("/publish", data=d, crossdomain=false)
    //also using jquery for requests is like using an elephant gun to kill gophers

    
}


// function deviceMoved() {
//     r = map(accelerationX, -90, 90, 100, 175);
//     g = map(accelerationY, -90, 90, 100, 200);
//     b = map(accelerationZ, -90, 90, 100, 200);
//   }