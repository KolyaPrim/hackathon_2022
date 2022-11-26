let poll_submit_btn = document.getElementById("poll_submit_btn")
let inputs_list = $("#inputs_container input")
let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value
let inputs_div = document.getElementById("inputs_div")
let thanks_div = document.getElementById("thanks_div")
poll_submit_btn.onclick = function (){
    let inputs_data = []
    for (let input of inputs_list){
        let type = input.type
        if (type!=="text" && !input.checked){
            continue
        }
        inputs_data.push({
            "value":input.value,
            "id":input.id,
            "question_id":input.getAttribute('question_id'),
            "poll_id":input.getAttribute('poll_id'),
            "type":type
        })
    }
    $.ajax({
        url: "/api/answer/",
        type: "POST",
        headers: {
            "X-CSRFToken": csrf,
        },
        data: {
            "inputs_data": JSON.stringify(inputs_data)
        },
        success: function (data) {
            inputs_div.classList.add("d-none");
            thanks_div.classList.remove("d-none");
        },
        error: function (xhr, errmsg, err) {
            console.log("not success");
        }
    });
}