/**
 * Created by vt on 15/3/13.
 */

$(function () {
    var $errMsg = $('#loginErrorMsg');
    $('.ui.form').form({
        username: {
            identifier: 'email',
            rules: [
                {
                    type: 'empty',
                    prompt: 'Please enter a email'
                }, {
                    type: 'email',
                    prompt: 'Please enter a valid email'
                }
            ]
        },
        password: {
            identifier: 'password',
            rules: [
                {
                    type: 'empty',
                    prompt: 'Please enter a password'
                },
                {
                    type: 'length[6]',
                    prompt: 'Your password must be at least 6 characters'
                }
            ]
        }
    }, {
        inline: true,
        on: 'blur',
        onSuccess: function (e) {
            $errMsg.fadeOut();
            var $form = $(this).addClass('loading');
            e.preventDefault();
            var datas = $form.form('get values');
            datas.password = md5(datas.password);
            $.ajax({
                url: '/admin/login', data: datas, type: "POST"
            }).done(function (res) {
                if (res.code === 200) {
                    return window.location.replace("/admin");
                }
                $errMsg.fadeIn();
                $errMsg.children('p').text(res.message);
            }).always(function () {
                $form.removeClass('loading');
            });
        }
    });
});