
    $("#editComment").on("show.bs.modal", function (e) {
        var button = $(e.relatedTarget)
        var action = button.data('action')
        var modal = $(this)
        modal.find("#form").attr('action', action)
        modal.find("#comment").val(button.data('message'))
        modal.find("#header").text(button.data('header'))
        modal.find("#submit_button").text(button.data('button'))
    });
    
$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this?');
})

// $("#update_btn").click(function(){
//     $("#update_btn").hide();
//     $("#save_btn").show();
//     $(".editContext").each(function(){
//         var value = $(this).text();
//         // var types = $(this).data('type')
//         var data = "<input type='text' name='' class='form-control input_ input_data' value='"+value+"'>";
//         $(this).html(data);
//     });
// });
// $("#save_btn").click(function(){
//     $("#save_btn").hide();
//     $("#update_btn").show();
//     var json_data = [];
//     $(".input_data").each(function(){
//         var value = $(this).val();
//         var parent_html = $(this).parent();
//         parent_html.html(value);
//         $(this).remove();
//     });
//     $(".editContext").each(function(){
//         var context = $(this).text();
//         var single_data={"context":context}
//         json_data.push(single_data);
//     });
//     var string_data = JSON.stringify(json_data)
//     $.ajax({
//         url:'{% url "edit_comment" %}',
//         type: 'POST',
//         headers: {
//             "X-CSRFToken": '{{csrf_token}}'
//        },
//         data:{
//             data:string_data,
//         }
//     })
// })
