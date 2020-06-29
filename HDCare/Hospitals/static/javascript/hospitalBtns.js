// delete comment

$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this comment?');
})

// function get cookie of csrftoken

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// update comment
$(".update_btn").click(function(){
    $(this).hide();
    $(this).next().show();

    $(this).parent().parent().next().children('.editContext').val(function(){
        var value = $(this).text();
        var data = "<input type='text' class='form-control input_data' value='"+value+"'>";
        $(this).html(data);
    });
});
$(".save_btn").click(function(){
    $(this).hide();
    $(this).prev().show()
    var json_data = [];
    $(".input_data").val(function(){
        var context = $(this).val();
        var parent_html = $(this).parent();
        parent_html.html(context);
        $(this).remove();
    });
    $(this).parent().parent().next().children('.editContext').val(function(){
        var context = $(this).text();
        var single_data = context;
        json_data.push(single_data);
    });
    var string_data = json_data[0]
    $.ajax({
        url:$(this).attr("url"),
        type: 'POST',
        data:{
            data:string_data,
            csrfmiddlewaretoken: csrftoken,
        }
    })
})

// update specialize
$(".update_btn").click(function(){
    $(this).hide();
    $(this).next().show()
    $(this).parent().prev('div').val(function(){
        var value = $(this).text();
        var data = "<input type='text' class='form-control input_data' value='"+value+"'>";
        $(this).html(data);
        
    });
});
$(".save_btn").click(function(){
    $(this).hide();
    $(this).prev().show()
    var json_data = [];
    $(".input_data").val(function(){
        var speciality = $(this).val();
        var parent_html = $(this).parent();
        parent_html.html(speciality);
        $(this).remove();
    });
    $(this).parent().prev('div').val(function(){
        var speciality = $(this).text();
        var single_data = speciality;
        json_data.push(single_data);
    });
    var string_data = json_data[0]
    $.ajax({
        url:$(this).attr("url"),
        type: 'POST',
        data:{
            data:string_data,
            csrfmiddlewaretoken: csrftoken,
        }
    })
})