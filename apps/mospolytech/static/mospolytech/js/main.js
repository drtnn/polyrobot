(function ($) {
    "use strict";
    var myModal = {
        open(emoji, text) {
            const modal = document.getElementById('loginResponseModal')
            modal.setAttribute('aria-hidden', 'false')
            modal.classList.remove('fade')
            modal.style.display = 'flex'

            modal.querySelectorAll('[data-bs-dismiss="modal"]').forEach(item => item.onclick = this.close.bind(this))
            modal.querySelector('.modal-emoji').innerText = emoji
            modal.querySelector('.modal-text').innerText = text

            $(".wrap-login100").hide()
        },
        close() {
            const modal = document.getElementById('loginResponseModal')
            modal.setAttribute('aria-hidden', 'true')
            modal.classList.add('fade')
            modal.style.display = ''

            $(".wrap-login100").show()
        }
    }

    let input = $('.validate-input .input100');
    const pathname = window.location.pathname.split('/');
    const telegram = pathname[pathname.indexOf("login-to-mospolytech") + 1];

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
                    myModal.open("✅️", "Авторизация прошла успешно!");
                })
                .fail(function () {
                    myModal.open("❗️", "Неверный логин или пароль!");
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