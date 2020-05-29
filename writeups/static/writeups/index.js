// Using Jquery to remove inline css from WYSIWYG generated HTML.

$("img").attr('style', '');
hljs.initHighlightingOnLoad();

$("label[for = 'id_text']").html("<b> Comment </b>");
$(".reply-comments").find("label[for = 'id_text']").html("<b> Reply </b>");

function showhidereply(btn) {

    let replyDiv = document.getElementById("reply-id");

    if (btn.value == "show") {

        replyDiv.style.display = "block";
        btn.value = "hide";
    } else {

        replyDiv.style.display = "none";
        btn.value = "show";
    }
}

/*
$(document).ready(function (event) {

    $(document).on('click', '#like', function (event) {

        event.preventDefault();
        let pk = $(this).attr('value');

        $.ajax({
            type: 'POST',
            url: "{% url 'like' post.id post.slug %}",
            // url: "like",
            data: {
                'post_id': pk,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            dataType: 'json',
            success: function (response) {
                $('#like_section').html(response['form'])
                console.log($('#like_section').html(response['form']));
            },
            error: function (response, e) {
                console.log(response.responseText);
            }
        });
    })
});
*/
