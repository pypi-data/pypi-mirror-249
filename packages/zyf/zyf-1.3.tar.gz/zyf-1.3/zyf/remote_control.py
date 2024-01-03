# -*- coding: utf-8 -*-
"""
DateTime: 2024/1/2 11:21
Author  : ZhangYafei
Description:
使用示例：
    client = ParamikoHelper(hostname=hostname, username=username, password=password)
    content, code = client.exec_command("display ip interface brief")
    client.__close__()
    print(content, code)
"""
import socket
import paramiko


class ParamikoHelper:
    """ 远程设备操作 """
    def __init__(self, hostname: str, username: str, password: str, port: int = 22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self._ssh_client = self.build_connect(hostname=hostname, username=username, password=password, port=port)

    def build_connect(self, hostname: str, username: str, password: str, port: int = 22):
        """
        建立连接
        :param hostname:
        :param username:
        :param password:
        :param port:
        :return: ssh_client
        """
        ssh_client = paramiko.SSHClient()
        # 如果之前没有连接过的ip，会出现选择yes或者no的操作， 自动选择yes
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
        return ssh_client

    def login_verify(self, username: str, password: str):
        """
        登录校验
        :param hostname:
        :param username:
        :param password:
        :return:
        """
        ssh_client = paramiko.SSHClient()  # 调用paramiko的SSHClient方法连接网络设备，及本地设备为客户端
        connect_res = {'hostname': self.hostname, 'username': username, 'password': password, 'success': False,
                       'info': None}
        try:
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=self.hostname, username=username,
                               password=password)  # 调用connect()方法，输入连接设备所需的ip，用户名，密码
            ssh_client.close()
            connect_res['success'] = True
            connect_res['info'] = f"连接成功"
        except paramiko.ssh_exception.NoValidConnectionsError:
            connect_res['info'] = '连接失败，用户不存在'
        except paramiko.ssh_exception.AuthenticationException:
            connect_res['info'] = "连接失败，密码错误"
        except socket.error:
            connect_res['info'] = "连接失败，socket.error"
        except Exception as e:
            connect_res['info'] = f"连接失败，{e}"
        return connect_res

    def exec_command(self, command: str):
        """
        执行命令
        :param command:
        :return:
        """
        stdin, stdout, stderr = self._ssh_client.exec_command(command=command)
        result = stdout.read().decode('utf-8')
        code = stdout.channel.recv_exit_status()
        return result, code

    def download_file(self, remotepath: str, localpath: str):
        """
        远程下载文件
        :param remotepath:
        :param localpath:
        :return:
        """
        tran = self._ssh_client.get_transport()
        sftp = paramiko.SFTPClient.from_transport(tran)
        sftp.get(remotepath=remotepath, localpath=localpath)

    def put_file(self, localpath: str, remotepath: str):
        """
        远程上传文件
        :param localpath:
        :param remotepath:
        :return:
        """
        tran = paramiko.Transport(self.hostname, self.port)
        tran.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(tran)
        sftp.put(localpath=localpath, remotepath=remotepath)

    def __close__(self):
        self._ssh_client.close()