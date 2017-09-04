#!/usr/bin/env python
# -*- coding:utf-8 -*-
#----------------------------------------------
#@version:    ??                               
#@author:   Dylan_wu                                                        
#@software:    PyCharm                  
#@file:    main.py
#@time:    2017/6/28 11:21
#----------------------------------------------
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor,wait
import paramiko
import configparser
import os
import sys
import re
import pymysql
import prettytable
#====================从配置文件读取配置信息===============================
settings_path = os.path.join(os.pardir,'conf','settings')
config = configparser.ConfigParser()
config.read(settings_path)
ipaddr = config.get('database','ipaddr')
port = config.get('database','port')
username = config.get('database','username')
password = config.get('database','password')
database = config.get('database','database')
#=================================================SQL==============================================================
'''
-- user1的组名：
SELECT gname from user_info LEFT JOIN group_info on user_info.group_id = group_info.gid WHERE uname='user1'
-- user1管理的主机（包含user1属组的主机和user1的主机，并用UNION去重）：
SELECT host from u2h LEFT JOIN host_info on u2h.host_id = host_info.hid
LEFT JOIN user_info on u2h.user_id = user_info.uid WHERE uname='user1'
UNION
SELECT host from g2h LEFT JOIN host_info on g2h.host_id = host_info.hid
LEFT JOIN group_info on g2h.group_id = group_info.gid WHERE gname = 'IT'
-- IT组的主机：
SELECT host from g2h LEFT JOIN host_info on g2h.host_id = host_info.hid
LEFT JOIN group_info on g2h.group_id = group_info.gid WHERE gname = 'IT'
'''
login_sql = 'select * from user_info where uname=%s and pwd=%s'
gname_sql = 'SELECT gname from user_info LEFT JOIN group_info on user_info.group_id = group_info.gid WHERE uname=%s'

host_list_sql = 'SELECT host_info.host,host_info.ip,host_info.user,host_info.pwd from u2h LEFT JOIN host_info on u2h.host_id = host_info.hid LEFT JOIN user_info on u2h.user_id = user_info.uid WHERE uname=%s UNION SELECT host_info.host,host_info.ip,host_info.user,host_info.pwd from g2h LEFT JOIN host_info on g2h.host_id = host_info.hid LEFT JOIN group_info on g2h.group_id = group_info.gid WHERE gname=%s'

g_host_sql = 'SELECT host_info.host,host_info.ip,host_info.user,host_info.pwd from g2h LEFT JOIN host_info on g2h.host_id = host_info.hid LEFT JOIN group_info on g2h.group_id = group_info.gid WHERE gname = %s'

g_sql = 'SELECT host_info.host,host_info.ip,host_info.user,host_info.pwd from g2h LEFT JOIN host_info on g2h.host_id = host_info.hid LEFT JOIN group_info on g2h.group_id = group_info.gid WHERE gname = %s'

#==================================================================================================================
def login():
    user = input('请输入用户名:').strip()
    pwd = input('请输入密码：').strip()
    res = sql_helper(login_sql,user,pwd)
    return res

def show_user_info(res):
    usrname = res[0]['uname']
    group_name_list = sql_helper(gname_sql,usrname)

    host_list = []
    for g_name in group_name_list:
        h_res = sql_helper(host_list_sql,usrname,g_name['gname'])
        host_list += h_res

    print('当前用户：%s 属组：%s'%(usrname,[i['gname'] for i in group_name_list]))

    print('用户管理的主机：')
    host_table = prettytable.PrettyTable()
    host_table.field_names = ['host', 'ip', 'username','password']
    for host_info in host_list:
        host_table.add_row([host_info['host'], host_info['ip'], host_info['user'],host_info['pwd']])
    print(host_table)
    return host_list,[i['gname'] for i in group_name_list][0]

def sql_helper(sql,*args):
    conn = pymysql.Connect(host=ipaddr,
                           port=int(port),
                           user=username,
                           password=password,
                           database=database,
                           charset='utf8'
                           )


    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,list(args))
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def cmd_mode(host_info,cmd):
    host = host_info['host']
    ip = host_info['ip']
    username = host_info['user']
    passwd = host_info['pwd']
    ssh_obj = paramiko.SSHClient()
    ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_obj.connect(ip,22,username,passwd)
    stdin,stdout,stderr = ssh_obj.exec_command(cmd)
    # if stderr:
    #     print(stderr.read().decode('utf-8'))
    # else:
    res = stdout.read().decode('utf-8')
    print('\033[32;1m<%s> from %s:%s\033[0m'%(cmd,host,ip))
    print(res)
    ssh_obj.close()

def scp_mode(host_info,mode,local_file,remote_path):
    print(local_file,os.path.join(remote_path,os.path.basename(local_file)))
    ip = host_info['ip']
    username = host_info['user']
    passwd = host_info['pwd']
    t = paramiko.Transport((ip,22))
    t.connect(username=username,password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put(localpath=local_file,remotepath=os.path.join(remote_path,os.path.basename(local_file)))
    t.close()
    print('send %s to %s%s successed!'%(os.path.basename(local_file),ip,remote_path))

def run():
# if __name__ == '__main__':
    while True:
        res = login()
        if res:
            # print(res)
            print('登录成功')
            host_list,group_name = show_user_info(res)
            while True:
                try:
                    enter_str = input('>>:')
                    input_cmd = enter_str.strip().split()
                    match_host_list = []
                    if '-h' in input_cmd:  # 将-h后的主机名添加到match_host_list
                        host_names = input_cmd[input_cmd.index('-h') + 1].strip().split(',')
                        for h_name in host_names:
                            if h_name in [h_info['host'] for h_info in host_list]:
                                match_host_list.append(h_name)


                    if '-g' in input_cmd:  # 将-g后的主机名添加到match_host_list
                        group_names = input_cmd[input_cmd.index('-g') + 1].strip().split(',')
                        for g_name in group_names:
                            if g_name == group_name:
                                g_host_list = sql_helper(g_sql,group_name)
                                match_host_list += [g_host['host'] for g_host in g_host_list]
                    if '-all' in input_cmd:
                        match_host_list += [h_info['host'] for h_info in host_list]
                    # print(set(match_host_list))
                    if input_cmd[0] == 'batch_run' and '-cmd' in input_cmd:
                        cmd = re.findall('"(.*)"', enter_str)[0].strip()
                        if cmd.startswith('rm'):
                            print('\033[31;1mYou can not run cmd <rm>!\033[0m')
                            continue  # 不能输入rm命令
                        print('run <%s>....' % cmd)
                        pool = ThreadPoolExecutor(5)
                        f_list = []
                        for host_info in host_list:
                            for host in set(match_host_list):  # 去除重复的主机
                                if host == host_info['host']:
                                    future = pool.submit(cmd_mode,host_info,cmd)
                                    f_list.append(future)
                        wait(f_list)
                        # p_list = []
                        # p = Pool()
                        # for host_info in host_list:
                        #     for host in set(match_host_list):  # 去除重复的主机
                        #         if host == host_info['host']:
                        #             p.apply_async(cmd_mode,args=(host_info,cmd))
                        # p.close()
                        # p.join()

                    elif input_cmd[0] == 'batch_scp':
                        local_file = input_cmd[input_cmd.index('-local') + 1]
                        remote_path = input_cmd[input_cmd.index('-remote') + 1]
                        mode = input_cmd[input_cmd.index('-action') + 1]
                        pool = ThreadPoolExecutor(5)
                        f_list = []
                        for host_info in host_list:
                            for host in set(match_host_list): # 去除重复的主机
                                if host == host_info['host']:
                                    future = pool.submit(scp_mode,host_info,mode,local_file,remote_path)
                                    f_list.append(future)
                        wait(f_list)
                        # p = Pool()
                        # for host_info in host_list:
                        #     for host in set(match_host_list): # 去除重复的主机
                        #         if host == host_info['host']:
                        #             p.apply_async(scp_mode, args=(host_info, mode, local_file, remote_path))
                        # p.close()
                        # p.join()

                    elif input_cmd[0] == 'quit':
                        break

                    else:
                        print('usage: batch_run -h [host...] -g [server_group...] -cmd "cmd"')
                        print(
                            'usage: batch_scp -h [host...] -g [server_group...] -action put -local local_file -remote remote_path')
                except Exception as e:
                    print(e)
                    print('usage: batch_run -h [host...] -g [server_group...] -cmd "cmd"')
                    print(
                        'usage: batch_scp -h [host...] -g [server_group...] -action put -local local_path -remote remote_path')
        else:
            print('账号或密码错误！')



'''
if __name__ == '__main__':

    while True:
        try:
            enter_str = input('>>:')
            input_cmd = enter_str.strip().split()
            host_list = []
            if '-h' in  input_cmd : # 将-h后的主机名添加到host_list
                host_names = input_cmd[input_cmd.index('-h')+1].strip().split(',')
                for h_name in host_names:
                    if config.has_section(h_name.strip()):
                        host_list.append(h_name.strip())
                    else:
                        continue
                    # try:
                    #     host = config.get(h_name,'host').strip()
                    #     host_list.append(host)
                    # except configparser.NoSectionError:  # 不存在的主机名不会添加
                    #     continue

            if '-g' in input_cmd : # 将-g后的主机名添加到host_list
                group_names = input_cmd[input_cmd.index('-g')+1].strip().split(',')
                for g_name in group_names:
                    try:
                        group_host = config.get('server_group',g_name).strip().split(',')
                        host_list +=  group_host
                    except configparser.NoOptionError: # 不存在的主机名不会添加
                        continue
            # print(host_list)
            if input_cmd[0] == 'batch_run' and '-cmd' in input_cmd :
                cmd = re.findall('"(.*)"',enter_str)[0].strip()
                if cmd.startswith('rm'):
                    print('\033[31;1mYou can not run cmd <rm>!\033[0m')
                    continue # 不能输入rm命令
                print('run <%s>....'%cmd)
                # p_list = []
                p = Pool()
                for host in set(host_list): # 去除重复的主机
                    res = p.apply_async(cmd_mode,args=(host,cmd))
                #     p_list.append(res)
                #
                # for p in p_list:
                #     p.get()
                p.close()
                p.join()

            elif input_cmd[0] == 'batch_scp':
                local_file = input_cmd[input_cmd.index('-local')+1]
                remote_path = input_cmd[input_cmd.index('-remote')+1]
                mode = input_cmd[input_cmd.index('-action')+1]
                p = Pool()
                for host in set(host_list):
                    res = p.apply_async(scp_mode, args=(host, mode,local_file,remote_path))
                p.close()
                p.join()

            elif input_cmd[0] == 'quit':
                break

            else:
                print('usage: batch_run -h [host...] -g [server_group...] -cmd "cmd"')
                print('usage: batch_scp -h [host...] -g [server_group...] -action put -local local_file -remote remote_path')
        except Exception as e:
            print(e)
            print('usage: batch_run -h [host...] -g [server_group...] -cmd "cmd"')
            print(
                'usage: batch_scp -h [host...] -g [server_group...] -action put -local local_path -remote remote_path')
'''



















