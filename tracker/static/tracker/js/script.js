// function alterAddRemove(obj) {
//     let add_remove_btn = document.getElementById("add_remove_btn");
//     if (add_remove_btn.value === "add") {
//         add_remove_btn.className = "btn btn-sm btn-danger";
//         add_remove_btn.value = "remove";
//         add_remove_btn.innerHTML = "Remove";
//     } else if (add_remove_btn.value === "remove") {
//         add_remove_btn.className = "btn btn-sm btn-success";
//         add_remove_btn.value = "add";
//         add_remove_btn.innerHTML = "Add";
//     }
// }

// $(function() {
//     $("#add_remove_form").submit(function(event) {
//         event.preventDefault();
//         let addRemoveForm = $(this);
//         let posting = $.post(addRemoveForm.attr('action'), addRemoveForm.serialize() );
//         posting.done(function(data){
//             //change button maybe?
//         });
//         posting.fail(function(data){
//             //4xx or 5xx response
//         });
//     });
// });

$(document).on('click', '.btn-add-remove', function(e) {
    let value = $(this).val();
    let formAction = $(this.form).attr('action');
    console.log(formAction);
    console.log(value);
    $.ajax({
        url: formAction,
        type: "POST",
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            alter_show_list: value
        }
    });
    if (value === "add") {
        $(this).removeClass("btn-success");
        $(this).addClass("btn-danger");
        $(this).val("remove");
        $(this).html("Remove");
    } else if (value === "remove") {
        $(this).removeClass("btn-danger");
        $(this).addClass("btn-success");
        $(this).val("add");
        $(this).html("Add");
    }
    e.preventDefault();
    return false;
});

// function submit(obj) {
//     let xhr = new XMLHttpRequest();
//     let action = document.getElementById("add_remove").action;
//     xhr.open('POST', action);
//     xhr.onload = function() {
//         if (xhr.status !== 200) {
//             alert('Request failed.  Returned status of ' + xhr.status);
//         }
//     };
//
// }