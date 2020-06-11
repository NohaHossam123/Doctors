
    $("#editReview").on("show.bs.modal", function (e) {
        var button = $(e.relatedTarget)
        var action = button.data('action')
        var modal = $(this)
        modal.find("#form").attr('action', action)
        modal.find("#review").val(button.data('message'))
        modal.find("#header").text(button.data('header'))
        modal.find("#edit_button").text(button.data('button'))
    });
    
$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this review?');
})