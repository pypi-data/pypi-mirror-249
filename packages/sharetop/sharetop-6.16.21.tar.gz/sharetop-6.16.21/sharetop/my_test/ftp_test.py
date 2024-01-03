from typing import Dict, Optional

from ftplib import FTP

# 创建FTP对象
# ftp = FTP()
#
# # 连接FTP服务器
# ftp.connect('183.6.56.70', 2121)
#
# # 登录FTP服务器
# ftp.login('ftp-ths-read', 'i!9|j3pB')
#
# ftp.cwd("/2023-12-25/insert")
#
# # 执行FTP操作
# # 例如，列出FTP服务器上的文件
# ftp.retrlines('LIST')
# # 关闭连接
# ftp.quit()



# def get_filelist(hostname, username, password):
#     # 连接到FTP服务器
#     try:
#         ftp = FTP()
#         ftp.connect(hostname, 2121)
#         ftp.login(username, password)
#         # 切换到指定目录
#         directory = '/2023-12-25/insert'  # 将此路径更改为所需的目录路径
#         ftp.cwd(directory)
#         # 获取当前目录下的文件列表
#         file_list = []
#         files = ftp.nlst()
#         for filename in files:
#             if not filename.startswith('.'):  # 如果不是隐藏文件则添加到列表中
#                 print("filename=======:", filename)
#                 # localfile = open(filename, "wb")
#                 # ftp.retrbinary(f"RETR {filename}", localfile.write)
#                 file_list.append(filename)
#         print("file_list=:", file_list)
#         for _ in file_list:
#             localfile = open(_, "wb")
#             ftp.retrbinary(f"RETR {_}", localfile.write)
#         return file_list, ftp
#     except Exception as e:
#         print("Error occurred while connecting to the FTP server.")
#         print(e)
#         return None
#     finally:
#         ftp.quit()

# 设置FTP服务器信息
# hostname = '183.6.56.70'
# username = 'ftp-ths-read'
# password = 'i!9|j3pB'

# 调用函数并打印结果
# result, ftp = get_filelist(hostname, username, password)
# if result is not None:
#     for filename in result:
#         print(filename)
#         # filename = "example.txt"
#         # path = f"/2023-12-25/insert/{filename}"
#         # print('path:', path)
#         # localfile = open(filename, "wb")
#         # ftp.retrbinary(f"RETR {filename}", localfile.write)
# else:
#     print("Failed to retrieve file list from FTP server.")
class FtpServe:
    def __init__(self, hostname: str, username: str, password: str, port: Optional[int] = 2121):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.ftp = self.ftp_obj()

    def ftp_obj(self):
        ftp = FTP()
        ftp.connect(self.hostname, self.port)
        ftp.login(self.username, self.password)
        return ftp

    def get_file(self, directory: str):
        # directory = '/2023-12-25/insert'  # 将此路径更改为所需的目录路径
        self.ftp.cwd(directory)
        # 获取当前目录下的文件列表
        file_list = []
        files = self.ftp.nlst()
        for filename in files:
            if not filename.startswith('.'):  # 如果不是隐藏文件则添加到列表中
                print("filename=======:", filename)
                # localfile = open(filename, "wb")
                # ftp.retrbinary(f"RETR {filename}", localfile.write)
                file_list.append(filename)
        print("file_list=:", file_list)
        for _ in file_list:
            localfile = open(_, "wb")
            # self.ftp.retrbinary(f"RETR {_}", localfile.write)
            self.ftp.retrlines(f"LIST {_}")


    def run(self, time_path: str):
        directory = f"{time_path}/insert"
        self.get_file(directory)



if __name__ == '__main__':
    hostname = '183.6.56.70'
    username = 'ftp-ths-read'
    password = 'i!9|j3pB'
    run_obj = FtpServe(hostname, username, password)
    time_path = "2023-12-26"
    run_obj.run(time_path)
