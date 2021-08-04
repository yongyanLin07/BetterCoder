$(function(){
    $("#collect").click(function(){
        if($("#collect").attr("src")=="../../static/images/collect.png")
			{
				$("#collect").attr("src","../../static/images/collect(1).png");
			}
			else
			{
				$("#collect").attr("src","../../static/images/collect.png");
			}
    });
})
    