###Intel Galileo weibo client使用说明

将autohome.py文件中的APP_KEY = ''和APP_SECRET = ''替换成自己在open.weibo.com中申请的秘钥，ACCOUNT和PASSWORD分别为微博账号和密码。

任意新建一个python文件

    #!/usr/bin/env python
    # coding=utf-8
    import autohome
    autohome.post("hello world it's from Intel Galileo @plantpark")

引号中为微博发送的内容，替换成你需要的内容即可。