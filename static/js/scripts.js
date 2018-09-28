function return_ajax_resp(url, other_data) {
    $.ajax({
        type: 'get',
        url: url,
        data: $.extend({ 'csrfmiddlewaretoken': getCookie('csrftoken') }, other_data),
        success: function (data, textStatus) {
            reload_rows(data);
        }
    });
}

function return_ref_data_ajax(url, other_data) {
    $.ajax({
        type: 'get',
        url: url,
        data: $.extend({ 'csrfmiddlewaretoken': getCookie('csrftoken') }, other_data),
        success: function (data, textStatus) {
            reload_rows(data);
        }
    });
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function reload_rows(data) {
    $("#table_row").empty();
    $("#table_row").html(data);
}


