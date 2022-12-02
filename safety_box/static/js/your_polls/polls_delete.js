function delete_poll(id,tag_id) {
    $.ajax({
        url: '/poll/delete/' + id + '/',
        headers: {
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
        },
        type: "POST",
        dataType: 'json',
        success: function (data) {
            document.getElementById('poll_' + id).remove()
            let length_block = $(`#block_tag_${tag_id} div[id^='poll_']`).length
            if(length_block === 0){
                 $(`#block_tag_${tag_id}`).remove()
            }
        },
        error: function (xhr, errmsg, err) {
            $('#modal_message_label').text('Error')
            $('#message_modal').modal('show')
        }
    })
}

window.delete_poll = delete_poll