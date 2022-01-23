

navigator.mediaDevices.getUserMedia({
    audio: true,
    video: false
  })
    .then(function(stream) {
      const audioContext = new AudioContext();
      const analyser = audioContext.createAnalyser();
      const microphone = audioContext.createMediaStreamSource(stream);
      const scriptProcessor = audioContext.createScriptProcessor(2048, 1, 1);
      const keyID = Math.floor(Math.random() * 1000); 
  
      analyser.smoothingTimeConstant = 0.8;
      analyser.fftSize = 1024;
        
      microphone.connect(analyser);
      analyser.connect(scriptProcessor);
      scriptProcessor.connect(audioContext.destination);
      scriptProcessor.onaudioprocess = function() {
        const array = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(array);
        const arraySum = array.reduce((a, value) => a + value, 0);
        const average = arraySum / array.length;
        console.log(Math.round(average));
        let vol = (Math.round(average));
        console.log(vol);
        
        d={"volume": vol, "keyID": keyID,}
        $.get("/publish", data=d, crossdomain=false)

        var canvas = document.getElementById('circle');
        if (canvas.getContext)
            {
                var ctx = canvas.getContext('2d'); 
                var X = canvas.width / 2;
                var Y = canvas.height / 2;
                var R = 45;
                ctx.beginPath();
                ctx.arc(X, Y, R, 0, 2 * Math.PI, false);
                ctx.lineWidth = 50;
                ctx.strokeStyle = '#dce6ac';
                ctx.stroke();    

            ctx.beginPath();
            ctx.arc(X, Y, R, 0, 2 * Math.PI, false);
            ctx.lineWidth = 20;
            ctx.strokeStyle = '#b1c071';
            ctx.stroke();

        }
      };
    })
    .catch(function(err) {
      /* handle the error */
      console.error(err);
    });

    function draw()
  {
var canvas = document.getElementById('circle');
if (canvas.getContext)
{
var ctx = canvas.getContext('2d'); 
var X = canvas.width / 2;
var Y = canvas.height / 2;
var R = 45;
ctx.beginPath();
ctx.arc(X, Y, R, 0, 2 * Math.PI, false);
ctx.lineWidth = 110;
ctx.strokeStyle = '#dce6ac';
ctx.stroke();
}
}

