const user_input = $("#hospitals-search")
const search_icon = $('#h-search-icon')
const hospitals = $('#h-replaceable-content')
const endpoint = '/hospitals/'

//search books
const book_input = $("#books_search")
const search = $("#search_icon")
const books = $("#replace-content")
const point = '/hospitals/addbook'

//search speciality
const speciality_input = $("#speciality_search")
const speciality_search = $("#search_speciality")
const specializations = $("#replaceable-content")
const speciality_point = '/hospitals/addspecialization'

//search reservations
const reservations_input = $("#reservations_search")
const icon_search = $("#search_icon")
const reservations = $("#replace_content")
const reservations_point = '/hospitals/reservation'

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

//function ajax to search book
let call = function (point, request_parameters) {
    $.getJSON(point, request_parameters)
        .done(response => {
            books.fadeTo('200', 0).promise().then(() => {
                books.html(response['html_from_view'])
                books.fadeTo('150', 1)
                search.removeClass('text-white')

            })
        })
}

//function ajax to search speciality
let ajax_speciality = function (speciality, request_parameters) {
    $.getJSON(speciality, request_parameters)
        .done(response => {
            specializations.fadeTo('200', 0).promise().then(() => {
                specializations.html(response['html_from_view'])
                specializations.fadeTo('150', 1)
                speciality_search.removeClass('text-white')

            })
        })
}

//function ajax to search reesrvations
let ajax_reservation = function (reservations_point, request_parameters) {
    $.getJSON(reservations_point, request_parameters)
        .done(response => {
            reservations.fadeTo('200', 0).promise().then(() => {
                reservations.html(response['html_from_view'])
                reservations.fadeTo('150', 1)
                icon_search.removeClass('text-white')

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


// search book
book_input.on('keyup', function () {

    const request_parameters = {
        q: $(this).val() 
    }

    search.addClass('text-white')

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(call, delay_by_in_ms, point, request_parameters)
});

// search speciality
speciality_input.on('keyup', function () {

    const request_parameters = {
        q: $(this).val() 
    }

    speciality_search.addClass('text-white')

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_speciality, delay_by_in_ms, speciality_point, request_parameters)
});

// search reservations
reservations_input.on('keyup', function () {

    const request_parameters = {
        r: $(this).val() 
    }

    icon_search.addClass('text-white')

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    scheduled_function = setTimeout(ajax_reservation, delay_by_in_ms,reservations_point , request_parameters)
});

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
