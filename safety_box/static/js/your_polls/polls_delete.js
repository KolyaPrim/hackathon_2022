function delete_poll(id) {
    $.ajax({
        url: '/poll/delete/' + id + '/',
        headers: {
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        type: "POST",
        dataType: 'json',
        success: function (data) {
            document.getElementById('poll_' + id).remove()
        },
        error: function (xhr, errmsg, err) {
            $('#modal_message_label').text('Error')
            $('#message_modal').modal('show')
        }
    })
}

window.delete_poll = delete_poll