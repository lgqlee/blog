/**
 * Created by vt on 15/3/13.
 */

$(function () {
    $('.ui.form').form({
        username: {
            identifier: 'email',
            rules: [
                {
                    type: 'empty',
                    prompt: 'Please enter a email'
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
        on: 'blur'
    });
});