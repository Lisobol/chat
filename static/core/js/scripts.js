
const messageTemplate = function({ id, author, time, text }) {
    `
    <div class="message" data-id="${id}">
        <div class="message_author">
            <div class="message_avatar"></div>
            <div class="message_name">${author}</div>
            <div class="message_time">${time}</div>
        </div>
        <div class="message_file">${file}</div>
        <div class="message_text">${text}</div>
    </div>
`;
};
$(document).ready(function() {
    var form = $('#message-form');
    var input = $('input[name=text]');
    var chat = $($('.chat')[0]);

    form.on('submit', function(e) {
        e.preventDefault();

        var formData = new FormData(e.target);

        $.post({
            // method: 'POST',
            url: '/message/',
            data: formData,
            processData: false,
            contentType: false,

            success: function(response) {
                // const renderedTemplate=messageTemplate(response.author,response.time,response.text, response.id)
                chat.prepend(response.renderedTemplate);
                input.val('');
            }
        })
    });

    setInterval(function() {
        const lastId = $('.message').first().data('id');

        $.get({
            url: '/chat/messages/',
            data: {
                last_id: lastId
            },

            success: function(response)  {
                if (response !== '') {
                    chat.prepend(response);
                }
            }
        })
    }, 5 * 1000);
});