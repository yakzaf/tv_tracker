$(document).on('click', '.btn-add-remove', function(e) {
    let value = $(this).val();
    let formAction = $(this.form).attr('action');
    $.ajax({
        url: formAction,
        type: "POST",
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            alter_show_list: value
        },
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