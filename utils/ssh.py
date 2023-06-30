import json
import logging
import boto3
import paramiko

import logging
from django.conf import settings
from django.http import JsonResponse

from contextlib import closing
# from django.co
# from ec2 import client
import datetime

date_time = datetime.datetime.now()
from django.conf import settings
import os

def update_password(channel, password):
    channel_data = str()
    status = True
    while status:
        if channel.recv_ready():
            channel_data = channel.recv(9999).decode("utf-8") 
        else:
            continue
        print(channel_data)
        if 'Last login:' in channel_data:
            channel.send('\n')

        elif 'centos' in channel_data:
            channel.send('sudo passwd root\n')

        elif 'New password' in channel_data:
            channel.send(f'{password}\n')

        elif 'Retype new password:' in channel_data:
            channel.send(f'{password}\n')

        # elif 'passwd: all authentication tokens updated successfully.' in channel_data:
        else:
            print("Password update successful")
            status = False


def update_3proxy(channel, port, username):
    print('Updating File')

    channel_data = str()
    status = True
    while status:
        if channel.recv_ready():
            channel_data = channel.recv(9999).decode("utf-8") 
        else:
            continue
        print(channel_data)
        if 'Last login:' in channel_data:
            print('switching User')
            channel.send('\n')
            channel.send('sudo su\n')

        elif 'root' in channel_data:
            text = "echo -e 'nscache 65536 \ndaemon\nusers username:CL:Vpsket4321\nauth strong\nallow *\nproxy -p6700 -a\nsetgid 99\nsetuid 99'  >> 3proxy.cfg".format(username, port)
            print('Updating file')
            # channel.send('cd /etc\n')
            print("Changed directory")
            channel.send("> 3proxy.cfg \n")
            channel.send("echo -e 'nscache 65534\ndaemon\nusers {}:CL:Vpsket4321\nauth strong\nallow *\nproxy -p{} -a\nsetgid 99\nsetuid 67' > /etc/3proxy.cfg".format(username, port))


            # channel.send("echo 'nscache 65536' >> 3proxy.cfg \n")
            # channel.send("echo 'daemon' >> 3proxy.cfg \n")
            # channel.send("echo 'users {}:CL:Vpsket4321' >> 3proxy.cfg \n".format(username))
            # channel.send("echo 'auth strong' >> 3proxy.cfg \n")
            # channel.send("echo 'allow *' >> 3proxy.cfg \n")
            # channel.send("echo 'proxy -p{} -a' >> 3proxy.cfg \n".format(port))
            # channel.send("echo 'setgid 99' >> 3proxy.cfg \n")
            # channel.send("echo 'setuid 99' >> 3proxy.cfg \n")
            print("Restarting 3Proxy")
            channel.send("sudo systemctl restart 3proxy \n")
            channel.send('cat 3proxy.cfg \n')
            status = False


def delete_3proxy(channel):
    print('Delete File')

    channel_data = str()
    status = True
    while status:
        if channel.recv_ready():
            channel_data = channel.recv(9999).decode("utf-8") 
        else:
            continue
        print(channel_data)
        if 'Last login:' in channel_data:
            print('switching User')
            channel.send('\n')
            channel.send('sudo su\n')
            print('Deleting file')
            channel.send('cd /etc\n')
            channel.send('rm 3proxy.cfg \n')
        elif 'rm: remove regular' in channel_data:
            print('Deleted file')
            channel.send('y \n')
            channel.send('ls \n')
        
        else:
            print(channel_data)
            status = False




def update_3proxy_config(account, hostname, password, port, username):
    # print(account.ssh_key.path)
    print('Loading Key')
    k = paramiko.RSAKey.from_private_key_file(account.ssh_key.path)
    print("Key is loaded")
    c = paramiko.SSHClient()
    print('Instantiated Client')
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Starting connections")
    # c.connect( hostname = hostname, username = "centos", pkey = k)
    # channel = c.invoke_shell()
    # update_password(channel, password)
    # c.close()
    # print('Connecting')
    # c.connect( hostname = hostname, username = "centos", pkey = k)
    # channel = c.invoke_shell()
    # delete_3proxy(channel)
    # c.close()

    c.connect( hostname = hostname, username = "centos", pkey = k)
    print("connected")
    channel = c.invoke_shell()
    update_3proxy(channel, port, username)
    c.close()

    return 




def update_instance_through_ssh(client, account, instance):
    from random import randrange
    description = instance.describe_instance(client)
    host = description['Instances'][0]["PublicIpAddress"]
    print(description)
    print(host)
    key = account.ssh_key
    password = account.password
    # if account.password == 'centos':
    password = 'Vpsket4321'
    
    port = randrange(31000,60000)
    username = account.username
    # if account.username == 'centos':
    username = 'awspuser'
    print('Starting Process')
    update_3proxy_config(account, host, password, port, username)
    return port, username, password



if __name__ == '__main__':
    print('Updating Password')
    # print(account.ssh_key.path)
    # k = paramiko.RSAKey.from_private_key_file(account.ssh_key.path)
    k = paramiko.RSAKey.from_private_key_file(os.path.join(os.getcwd(), 'awsproxykey.pem'))
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # c.connect( hostname = '15.207.120.172', username = "centos", pkey = k)
    # channel = c.invoke_shell()
    # update_password(channel, 'Err@56@ty12345TY')
    # c.close()

    # c.connect( hostname = '15.207.120.172', username = "centos", pkey = k)
    # channel = c.invoke_shell()
    # delete_3proxy(channel)
    # c.close()
    
    c.connect( hostname = '15.207.120.172', username = "centos", pkey = k)
    print('connected')
    channel = c.invoke_shell()
    update_3proxy(channel, 4510, 'MATUTU')
    c.close()
