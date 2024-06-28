$(document).ready(function(){
    $('#chat-form').on('submit', function(event){
        event.preventDefault();
        const message = $('#message').val();
        $('#chat-box').append('<div class="message sent"><div class="text">' + message + '</div></div>');
        $.ajax({
            url: "support",
            method: "POST",
            data: $(this).serialize(),
            success: function(data){
                $('#chat-box').append('<div class="message received"><div class="text">' + data.response + '</div></div>');
                $('#message').val('');
                $('#chat-box').scrollTop($('#chat-box')[0].scrollHeight);
            }
        });
    });
});