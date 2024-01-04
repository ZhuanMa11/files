# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_KyoRyu'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 KyoRyu
# 日期: 2022/10/18
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import datetime
import os
import tarfile
import zipfile
from shutil import copyfile
import py7zr


class CommonFileOperate:

    @staticmethod
    def copy_file(file_path, ext):
        """
        copy文件
        :param file_path: 源文件路径
        :param ext: 后缀
        :return: 新文件的路径
        """
        new_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        target_path = file_path.rsplit('/', 1)[0] + "/{0}.{1}".format(new_name, ext)
        copyfile(file_path, target_path)
        return target_path, new_name

    @staticmethod
    def dwg_compressed_package(file_path, ext):
        """
        地址解压
        @param ext: 后缀名
        @param file_path:文件路径
        """
        document_path = file_path.rsplit('.', 1)[0]
        if ext == "zip":
            CommonFileOperate._un_zip(file_path, document_path)
        elif ext == "7z":
            CommonFileOperate._un_7z(file_path, document_path)
        elif ext == "tar":
            CommonFileOperate._un_tar(file_path, document_path)
        else:
            pass

    @staticmethod
    def _un_zip(file_name, document_path_name):
        """unzip zip file"""
        zip_file = zipfile.ZipFile(file_name)
        if os.path.isdir(document_path_name):
            pass
        else:
            os.mkdir(document_path_name)
        for names in zip_file.namelist():
            zip_file.extract(names, document_path_name)
        zip_file.close()
        CommonFileOperate._change_name(document_path_name)

    @staticmethod
    def _un_7z(file_name, document_path_name):
        """un_7z 7z file"""
        archive = py7zr.SevenZipFile(file_name, mode='r')
        archive.extractall(path=document_path_name)
        archive.close()

    @staticmethod
    def _un_tar(file_name, document_path_name):
        """解压 tar 文件"""
        tar = tarfile.open(file_name)
        names = tar.getnames()
        if os.path.isdir(document_path_name):
            pass
        else:
            os.mkdir(document_path_name)
            # 因为解压后是很多文件，预先建立同名目录
        for name in names:
            tar.extract(name, document_path_name)
        tar.close()

    @staticmethod
    def _change_name(filename):
        os.chdir(filename)
        for i in os.listdir("."):
            try:
                test_name = i.encode("cp437")
                test_name = test_name.decode("gbk")  # 将文件名转为gbk中文编码
                os.rename(i, test_name)  # 重命名
                i = test_name
            except:
                pass
            if os.path.isdir(i):  # 如果解压后的是一个文件夹
                CommonFileOperate._change_name(i)
                os.chdir('..')
