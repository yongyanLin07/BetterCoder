/* In order to get csrftoken in js file */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
/* get the csrf token */
var csrftoken = getCookie('csrftoken');
/* using ajax to delete the mark/comment/like if the user want */
function deleteList(current_elem, id){
    var status = confirm("Are you sure you want to delete it?");
    if(!status){
        return false;
    }
    $.ajax({
        cache: false,
        type: "POST",
        url: current_elem.data('url'),
        data:{'id':id},
        async: false,
        beforeSend:function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(data) {
            if(data.status == 'fail'){
                if(data.msg == 'Please login'){
                    window.location.href="{% url 'rango:login' %}";
                }else{
                    current_elem.text(data.msg)
                }

            }else if(data.status == 'success'){
                current_elem.text(data.msg)
                window.location.href="{% url 'rango:profile_page' %}";
            }
        },
    });
}
/* using ajax to like/mark the news if the user want */
function change(current_elem, page_id){
    $.ajax({
        cache: false,
        type: "POST",
        url:current_elem.data('url'),
        data:{'page_id':page_id},
        async: false,
        beforeSend:function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(data) {
            if(data.status == 'fail'){
                if(data.msg == 'Please login'){
                    window.location.href="{% url 'rango:login' %}";
                }else{
                    current_elem.text(data.msg)
                }

            }else if(data.status == 'success'){
                current_elem.text(data.msg)
            }
        },
    });
}

$(document).ready(function() {
    /* call deleteList function by clicking the delete link */
    $('.delete').click(function() {
        var ID;
        ID = $(this).attr('data-id');
        deleteList($(this),ID);
    });
    /* call change function by clicking the thumb-up icon */
    $('#like_page_btn').click(function() {
        var pageIDVar;
        var i = $(this).attr("class");
        pageIDVar = $(this).attr('data-pageid');
        change($(this),pageIDVar);
        /* change the format of thumb-up icon */
        if(i == "iconfont icon-dianzan1"){
            $(this).attr("class","iconfont icon-dianzan");
        }else{
            $(this).attr("class","iconfont icon-dianzan1");
        }
    });
    /* call change function by clicking the thumb-up icon */
    $('#mark_page_btn').click(function() {
        var pageIDVar;
        var i = $(this).attr("class");
        pageIDVar = $(this).attr('data-pageid');
        change($(this),pageIDVar);
        /* change the format of star icon */
        if(i == "iconfont icon-shoucang6"){
            $(this).attr("class","iconfont icon-shoucang5");
        }else{
            $(this).attr("class","iconfont icon-shoucang6");
        }
    });
});
