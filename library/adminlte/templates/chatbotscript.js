<script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/2.0.4/socket.io.slim.js"></script>

<script type="text/javascript">

$( document ).ready(function() {
      var socket = io.connect('{{data['domain']}}');
      socket.on('connect', function() {
          console.log('connected');
      });

      socket.on('gps_update', function(message) {
          console.log(message.data.timestamp);
      });
 
      socket.on('disconnect', function() {
          console.log('disconnected');
      });

      socket.on('response', function(message) {
          console.log('response: ' + message);
          appendMessage(message, true);
      });




     function appendMessage( message , isBot) {
         var innerhtml = "<div class='item'>";
         if (isBot == true ) {
             innerhtml += "<img src='static/dist/img/user4-128x128.jpg' alt='user image'>";
             innerhtml += "<p class='message'>";
             innerhtml += "<a href='#' class='name'><small class='text-muted pull-right'><i class='fa fa-clock-o'></i> just now </small>Chat Bot</a>";
         } else {
             innerhtml += "<img src='static/dist/img/user3-128x128.jpg' alt='user image'>";
             innerhtml += "<p class='message'>";
             innerhtml += "<a href='#' class='name'><small class='text-muted pull-right'><i class='fa fa-clock-o'></i> just now </small>Me</a>";

         }
         innerhtml += message ;
         innerhtml += "</p></div>";
         $('#chat-box').append(innerhtml);

         $('#chat-box').animate({scrollTop: $('#chat-box').prop("scrollHeight")}, 500);
     }



     // add listener on text box
    $('#messageinput').keydown(function (event) {
        var keypressed = event.keyCode || event.which;
        if (keypressed == 13) {
            // pressed enter
            var message = $('#messageinput').val();
            console.log('got message => ' + message);
            appendMessage(message, false);
            socket.emit('message', message );
   
            $('#messageinput').val('');
            
        }
    });



});
</script>
