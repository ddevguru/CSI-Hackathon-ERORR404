$(document).ready(function() {
    function loadMessages() {
        $.get('/fetch_messages', function(data) {
            if (data.status === 'success') {
                $('#chat-box').empty();
                data.messages.forEach(function(msg) {
                    var messageClass = msg.sender_id === userId ? 'sent' : 'received';
                    $('#chat-box').append(
                        `<div class="${messageClass}">
                            <p><strong>Sender ${msg.sender_id}:</strong> ${msg.message}</p>
                            <small>${new Date(msg.timestamp).toLocaleString()}</small>
                        </div>`
                    );
                });
            }
        });
    }

    $('#send-button').click(function() {
        var message = $('#message-input').val();
        var receiverId = 1; // Replace with actual receiver ID

        if (message) {
            $.ajax({
                url: '/send_message',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    receiver_id: receiverId,
                    message: message
                }),
                success: function(data) {
                    if (data.status === 'success') {
                        $('#message-input').val('');
                        loadMessages();
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        }
    });

    loadMessages();
    setInterval(loadMessages, 5000); // Refresh messages every 5 seconds
});
