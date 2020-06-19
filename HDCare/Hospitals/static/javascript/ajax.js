const user_input = $("#hospitals-search")
const search_icon = $('#h-search-icon')
const hospitals = $('#h-replaceable-content')
const endpoint = '/hospitals/'
const delay_by_in_ms = 1000
let scheduled_function = false
let speciality_value = 'Specilizations';
let city_value = 'City';


let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            hospitals.fadeTo('200', 0).promise().then(() => {
                hospitals.html(response['html_from_view'])
                hospitals.fadeTo('150', 1)
                search_icon.removeClass('text-white')
                $('#options').val(speciality_value);
                $('#cities').val(city_value);

            })
        })
}


//all filter
$("body").on('click','#all',function () {

    speciality_value = 'Specilizations';
    city_value = 'City';

    const request_parameters = {
        a : "all"
    }
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
}) 


//search filter
user_input.on('keyup', function () {

    speciality_value = 'Specilizations';
    city_value = 'City'; 

    const request_parameters = {
        q: $(this).val() 
    }

    search_icon.addClass('text-white')

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
}) 




// specialty filter
$("body").on('change','#options',function () {

    let request_parameters;

    speciality_value = $(this).val()
    city_value = 'City'; 

    if($(this).val() == 'Specilizations'){
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
$("body").on('change','#cities',function () {
    let request_parameters;
    
    city_value = $(this).val()
    speciality_value = 'Specilizations'; 

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
