    $("#div_digg .action").click(function () {

        if ($(".info").attr("user")){
            var is_up = $(this).hasClass("diggit");
            // var article_id = $("#article_id").text();
            var article_id = $(".info").attr("article_id");
            var csrfmiddlewaretoken = $("[name='csrfmiddlewaretoken']").val()

            $.ajax({
                url:"/blog/up_down/",
                type:"post",
                data: {
                    is_up:is_up,
                    article_id:article_id,
                    csrfmiddlewaretoken : csrfmiddlewaretoken,
                },
                success: function (data) {
                    console.log(data);
                    if (data.state){
                        if(is_up){
                            var val = $("#digg_count").text();
                            val = parseInt(val)+1;
                            $("#digg_count").text(val);
                            $("#digg_tips").text("recommend suceeseful");
                        }else {
                            var val = $("#bury_count").text();
                            val = parseInt(val)+1;
                            $("#bury_count").text(val);
                            $("#digg_tips").text("dislike suceeseful");
                        }
                    }else{
                        if (data['is_updb']){
                            $("#digg_tips").html("recomment repeat");
                        }else{
                            $("#digg_tips").html("dislike repeat");
                        }

                        setTimeout(function () {
                            $("#digg_tips").html("");
                        }, 3000)
                    }
                }
            })
        }else{
            location.href="/login/"
        }


    })
