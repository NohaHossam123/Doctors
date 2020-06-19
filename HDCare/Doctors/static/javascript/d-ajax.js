// doctor search
const user_input = $("#doctors-search")
const search_icon = $('#d-search-icon')
const doctors = $('#d-replaceable-content')
const endpoint = '/doctors/'
const delay_by_in_ms = 1000
let scheduled_function = false
let speciality_value = 'Title';
let city_value = 'City';



let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            doctors.fadeTo('200', 0).promise().then(() => {
                doctors.html(response['html_from_view'])
                doctors.fadeTo('150', 1)
                search_icon.removeClass('text-white')
                $('#title').val(speciality_value);
                $('#city').val(city_value);

            })
        })
}


//all filter
$("body").on('click','#dall',function () {

    speciality_value = 'Title';
    city_value = 'City';

    const request_parameters = {
        a : "all"
    }
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
}); 


// search
user_input.on('keyup', function () {

    const request_parameters = {
        q: $(this).val() 
    }

    search_icon.addClass('text-white')

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
});




// specialty filter
$("body").on('change','#title',function () {

    let request_parameters;

    speciality_value = $(this).val()
    city_value = 'City'; 

    if($(this).val() == 'Title'){
         request_parameters = {
            a: $(this).val() 
        }
    }else{
        request_parameters = {
            s: $(this).val() 
        }
    }


    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)


}); 




//city filter
$("body").on('change','#city',function () {
    let request_parameters;
    
    city_value = $(this).val()
    speciality_value = 'Title'; 

    if($(this).val() == 'City'){
         request_parameters = {
            a: $(this).val() 
        }
    }else{
        request_parameters = {
            c: $(this).val() 
        }
    }


    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)


});
