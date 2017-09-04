一，关于batch_tools：
    1.使用navicat创建库名为s17day11homework的库，然后导入batch_tools/readme文件夹下的s17day11homework.sql
      在batch_tools/conf/settings配置要连接的数据库信息
    2.直接执行batch_tools/bin/start.py
    3.用户登录：
        user_info表默认包含3个用户：
            user1 pwd:123
            user2 pwd:456
            admin pwd:123456
    4.批量执行命令功能：
        如：batch_run -h host01,host02 -g IT  -cmd "hostname"
            -h : 用户管理的主机名
            -g ：用户属组名
            -all : 用户管理的所有主机
        (不能执行'rm'命令)
    5.批量上传功能：
        如：batch_scp -h host01,host02 -g IT -action put -local local_file -remote remote_path
        local_file为要上传的文件，如：/tmp/test_file.txt
        remote_path为指定的路径,如：/tmp/ （**注：路径下必须加/）
    3.退出：quit

二,博客地址：http://www.cnblogs.com/dylan-wu/articles/7142487.html