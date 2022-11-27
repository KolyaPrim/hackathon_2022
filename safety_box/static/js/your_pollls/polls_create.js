window.add_question = function () {
    let new_question = $('#question_0').clone()
    let questions = $('#questions')

    let new_el_id = questions.children().length + 1
    new_question.attr('id', `question_${new_el_id}`)
    questions.append(new_question)

    $(`#question_${new_el_id} #remove_btn_0`).attr('id', `remove_btn_${new_el_id}`)

    $(`#question_${new_el_id} #description_btn_0`).attr('id', `description_btn_${new_el_id}`)
    $(`#question_${new_el_id} #radio_btn_0`).attr('id', `radio_btn_${new_el_id}`)
    $(`#question_${new_el_id} #checkbox_btn_0`).attr('id', `checkbox_btn_${new_el_id}`)
    $(`#question_${new_el_id} #text_btn_0`).attr('id', `text_btn_${new_el_id}`)

    // $(`#question_${new_el_id} .description_container .remove_var_btn`).attr('id', `${new_el_id}_description_0`)
    // $(`#question_${new_el_id} .radio_container .remove_var_btn`).attr('id', `${new_el_id}_radio_0`)
    // $(`#question_${new_el_id} .checkbox_container .remove_var_btn`).attr('id', `${new_el_id}_checkbox_0`)
    // $(`#question_${new_el_id} .text_container .remove_var_btn`).attr('id', `${new_el_id}_text_0`)
    new_question.css({'display': 'block'})
    $('#submit_btn').css({'display': 'block'})
}

window.remove_question = function (e) {
    let id_el_to_delete = e.id.split('_')[2]
    $(`#question_${id_el_to_delete}`).remove()
    if ($('#questions').children().length === 0) {
        $('#submit_btn').css({'display': 'none'})
    }

}

window.add_variant = function (e) {

    let type = e.id.split('_')[0]
    let question_id = e.id.split('_')[2]
    let container_selector = `#question_${question_id} .${type}_container`
    let new_variant_id = $(container_selector).children().length + 1

    // $("#question_1 hr").css({'display': 'block'})

    if (!(type === 'description' && new_variant_id > 1)) {
        let new_el = $(`#input_${type}_0`).clone()
        new_el.attr('id', `input_${type}_${new_variant_id}`)
        new_el.css({'display': 'block'})
        $(`${container_selector}`).append(new_el)
    }
    $(`${container_selector} #input_${type}_${new_variant_id} .remove_var_btn`).attr('id', `${question_id}_${type}_${new_variant_id}`)

}

window.delete_variant = function (e) {
    let question_id = e.id.split('_')[0]
    // if ($(`#question_${question_id} .radio_container`).children().length === 2) {
    //       $("#question_1 hr").css({'display': 'none'})
    // }
    // else {
    //     let type = e.id.split('_')[1]
    //     let var_id = e.id.split('_')[2]
    //     $(`#question_${question_id} #input_${type}_${var_id}`).remove()
    // }
    let type = e.id.split('_')[1]
    let var_id = e.id.split('_')[2]
    $(`#question_${question_id} #input_${type}_${var_id}`).remove()
}

$('#submit_btn').click(function (e) {
    e.preventDefault()
    let if_required_fields_filled = document.getElementById('poll_create_form').reportValidity()
    let if_there_are_any_questions = Boolean($('#questions').children().length)
    if (if_required_fields_filled && if_there_are_any_questions) {
        submit()
    }
})

function submit () {
    let result = {
        'title': $('#poll_name')[0].value,
        'description': $('#poll_description')[0].value,
        'questions': []
    }
    let questions = $('#questions').children()
    questions.each(function (q_id, question) {
        let question_obj = {}
        let question_id = question.id
        question_obj['text'] = $(`#${question_id} .question_text`)[0].value
        question_obj['tag'] = $('#tag_input').val()
        try {
            question_obj['description'] = $(`#${question_id} .description_container textarea`)[0].value
        }
        catch (e) {
            console.log(e)
        }

        question_obj['variants'] = []

        $(`#${question_id} .checkbox_container`).children().each(function (v_id, variant) {
            let ch_id = variant.id
            let check_box_obj = {}
            check_box_obj['label'] = $(`#${question_id} .checkbox_container #${ch_id} .label_input`)[0].value
            check_box_obj['type'] = 'checkbox'
            question_obj['variants'].push(check_box_obj)
        })
        $(`#${question_id} .radio_container`).children().each(function (v_id, variant) {
            let rad_id = variant.id
            let radio_obj = {}
            radio_obj['label'] = $(`#${question_id} .radio_container #${rad_id} .label_input`)[0].value
            radio_obj['type'] = 'radio'
            question_obj['variants'].push(radio_obj)
        })
        $(`#${question_id} .text_container`).children().each(function (v_id, variant) {
            let text_id = variant.id
            let text_obj = {}
            text_obj['label'] = $(`#${question_id} .text_container #${text_id} .label_input`)[0].value
            text_obj['type'] = 'text'
            question_obj['variants'].push(text_obj)
        })

        result['questions'].push(question_obj)
    })
    console.log(result)
    post(result)
}

function post(data) {

    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
    let form_data = new FormData();
    // for (const [key, value] of Object.entries(data)) {
    //     form_data.append(key, value);
    // }
    form_data.append('data', JSON.stringify(data));
    for ( let file of $('#file_input')[0].files) {
        form_data.append('poll_css', file, data['title.css']);
    }
    $.ajax({
        // url: '/save_poll/',
        // headers: {
        //     'Content-type': 'application/json',
        //     'Accept': 'application/json',
        //     'X-CSRFToken': csrf
        // },
        // data: form_data,
        // files: $('#file_input')[0].files,
        // type: 'POST',
        // processData: false,  // tell jQuery not to process the data
        // contentType: false,

        type: "POST",
        url: '/save_poll/',
        headers: {
            // 'Content-type': 'application/json',
            // 'Accept': 'application/json',
            'X-CSRFToken': csrf
        },
        data: form_data,
        // data: {"inputs_data": JSON.stringify(data),
        // 'files':$('#file_input')[0].files},
        contentType: false,
        processData: false,
        cache: false,

        success: function (data) {
            console.log('success')
            console.log(data)
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg)
        }
    })
}

window.select_tag = function (el) {
    $('#tag_input').val(el.innerHTML)
}