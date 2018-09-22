// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
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
// var csrftoken = $("csrfmiddlewaretoken")

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({data: {
    csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val()
}});

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function post_login(){
    var username = $("#id_username").val();
    var password = $("#id_password").val();
    var loc = window.location;
    var endpoint = loc.pathname + loc.search
    $.post(endpoint, {"username": username,"password": password}, function(data) {
        if (data.meta.status_code == 200) { // ok
            window.location.replace(data.data.redirect_url)
        } else if (data.meta.status_code == 403) { // HTTP_403_FORBIDDEN
            alert("Your account is not active.")
        } else if (data.meta.status_code == 401) { // UNAUTHORIZED
            alert("username or password incorrect.")
        }
    });
}