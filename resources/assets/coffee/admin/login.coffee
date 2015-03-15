(($)->

  $errMsg = $('#loginErrorMsg')

  # 表单验证
  $('.ui.form').form({
    username:
      identifier: 'email'
      rules: [
        {
          type: 'empty'
          prompt: 'Please enter a email'
        }, {
          type: 'email'
          prompt: 'Please enter a valid email'
        }
      ]
    password:
      identifier: 'password'
      rules: [
        {
          type: 'empty'
          prompt: 'Please enter a password'
        }, {
          type: 'length[6]'
          prompt: 'Your password must be at least 6 characters'
        }
      ]

  },{

    inline: true
    on: 'blur',

    onSuccess: (e)->
      $errMsg.fadeOut();
      $form = $(this).addClass('loading')
      e.preventDefault()
      datas = $form.form('get values')
      # 对密码进行初步的 md5 加密后上传
      datas.password = md5(datas.password)
      $.ajax(
        url: '/admin/login'
        data: datas,
        type: 'POST'
      ).done((res)->
          # 如果返回 code 200 则完成跳转
          if res.code is 200
            return window.location.replace("/admin")
          $errMsg.fadeIn()
          $errMsg.children('p').text(res.message)
      ).always(()->
          $form.removeClass('loading')
      )
  })

)(jQuery)