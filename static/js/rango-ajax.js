function add_like(current_elem, page_id){
    $.ajax({
        cache: false,
        type: "POST",
        url:"localhost:8080/rango/like_page/",
        data:{'page_id':page_id},
        async: true,
        beforeSend:function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
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

function add_mark(current_elem, page_id){
    $.ajax({
        cache: false,
        type: "POST",
        url:"{% url 'rango:mark_page' %}",
        data:{'page_id':page_id},
        async: true,
        beforeSend:function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
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
    $('#like_page_btn').click(function() {
        var pageIDVar;
        var i = $(this).attr("class");
        pageIDVar = $(this).attr('data-pageid');
        add_like($(this),pageIDVar);

        if(i == "iconfont icon-dianzan3"){
            $(this).attr("class","iconfont icon-zan");
        }else{
            $(this).attr("class","iconfont icon-dianzan3");
        }
    });
});
$(document).ready(function() {
    $('#mark_page_btn').click(function() {
        var pageIDVar;
        var i = $(this).attr("class");
        pageIDVar = $(this).attr('data-pageid');
        add_mark($(this),pageIDVar);
        if(i == "iconfont icon-shoucang6"){
            $(this).attr("class","iconfont icon-shoucang5");
        }else{
            $(this).attr("class","iconfont icon-shoucang6");
        }
    });
});

