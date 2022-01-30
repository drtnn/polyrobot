(function ($) {
    "use strict";

    let input = $('.validate-input .input100');
    const pathname = window.location.pathname.split('/');
    const telegram = pathname[pathname.indexOf("login-to-mospolytech") + 1];
    console.log(telegram);

    $('.login100-form-btn').bind("click", function () {
        let check = true;

        for (let i = 0; i < input.length; i++) {
            if (validate(input[i]) === false) {
                showValidate(input[i]);
                check = false;
            }
        }

        if (!check) {
            return check;
        } else {
            return $.ajax({
                url: '/api/mospolytech/login-to-mospolytech/',
                dataType: 'json',
                type: 'POST',
                data: {
                    login: $('input[name=login]')[0].value,
                    password: $('input[name=password]')[0].value,
                    telegram: telegram
                }
            })
                .done(function () {
                    alert("success");
                })
                .fail(function () {
                    alert("error");
                })
        }
    });

    $('.validate-form .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });

    function validate(input) {
        return $(input).val().trim() !== '';
    }

    function showValidate(input) {
        let thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        let thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }


})(jQuery);