//get comment tree
// $.ajax({
//     url: "/blog/comment_tree/"+$(".info").attr("article_id")+'/',
//     type: "get",
//     success:function (data) {
//         console.log(data);
//         $.each(data, function (index, comment_dict) {
//             var s = '<div class="comment_item" comment_id="'+ comment_dict.pk +'">\n' +
//                 '            <span class="content">' + comment_dict.content + '</span>\n' +
//                 '        </div>';
//             if(comment_dict.parent_comment_id) {
//                 //chirld comment
//                 pid = comment_dict.parent_comment_id;
//                 $("[comment_id=" + pid + "]").append(s)
//             }
//             else{
//                 //root comment
//
//                 $(".comment_tree").append(s)
//             }
//         })
//     }
// })


var pid = '';

$("#comment_btn").click(function () {
    var data = {
        article: $(".info").attr("article_id"),
        user: $(".info").attr("user_id"),
        content:$("#comment_area").val(),
        parent_comment: pid,
        csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
    }
    if(pid){
        data.content = data.content.slice(data.content.indexOf('\n')+1);
        }
    $.ajax({
        url:"/blog/comment/",
        type: "post",
        data: data,
        success: function (data) {
            var create_time = data.create_time;
            var content = data.content;
            var username = $(".info").attr("user");
            var comment_li = '        <li class="list-group-item">\n' +
                '            <div>\n' +
                '                <span style="color: gray">' + create_time + '</span>\n' +
                '                &nbsp;&nbsp;\n' +
                '                <a href=""><span>' + username + '</span></a>\n' +
                '                <a href="" class="pull-right"><span>reply</span></a>\n' +
                '            </div>\n' +
                '            <div class="con">\n' +
                '                <p>\n' +
                '                    '+ content +'\n' +
                '                </p>\n' +
                '            </div>\n' +
                '        </li>'
            $(".comment_list").append(comment_li);
            //clear the textarea
            $("#comment_area").val("");
            pid = "";
        }
    })
})

$(".list-group-item .reply_btn").click(function () {
    $("textarea#comment_area").focus();
    var comment_author = '@' + $(this).attr("username") + '\n';
    $("textarea#comment_area").val(comment_author);
    pid = $(this).attr("pid");
    console.log(pid);
})
