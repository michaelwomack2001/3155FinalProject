$(document).ready(function() {

    $('button#delete').click(function(){
        window.location.href='/delete';
    })

    $("form").on('click','a',function(e) {
        e.preventDefault();
        var id = $(this).attr('id');
        
        $("input#" + id).prop("disabled", false);
        if (id === "password") {
            $("input#confirm_password").prop("disabled", false);
        }
    });
});