# -*- coding: utf-8 -*-
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# DTCloud v2.0
# QQ: 190066183
# 邮件: 190066183@qq.com
# 手机: 18118160329
# 作者: 'zyf_Flame'
# 公司网址: http://www.dtcloud360.com
# Copyright 中亿丰数字科技有限公司 2012-2022 Flame
# 日期: 2022/11/16
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
import datetime
import json
import os
import zipfile

import requests

import constants
import dtcloud
from dtcloud import fields, models, api

BACKUP_FOLDER = dtcloud.tools.config.get('addons_path').rsplit(',', 1)[-1]
TARGET_DIR = dtcloud.tools.config.get('file_backup_path')


class BackingUpFilesTask(models.Model):
    _name = "backing.up.files.task"
    _description = "备份文件"
    _order = 'id desc'

    name = fields.Char(string="名称")
    backup_file_path = fields.Char(string="备份文件路径")

    @api.model
    def clear_honor_files(self):
        """
        清理7天前的所有备份文件

        """
        domain = list()
        domain.append(('create_date', '<=', datetime.date.today() - datetime.timedelta(7)))
        records = self.sudo().search(domain)
        for rec in records:
            if os.path.exists(rec.backup_file_path):
                os.remove(rec.backup_file_path)
                rec.unlink()

    @api.model
    def get_file_id_list(self):
        """
        获取有关联关系的文件id列表
        """
        log_serve_url = dtcloud.tools.config.get('main_server_url')
        response = requests.get('%s/api/v1/business_file_res/file_ids' % log_serve_url)
        info = json.loads(response.text)
        file_id_list = list()
        if info["message"]['flag'] == 'info':
            for rec in info['data']:
                if rec['file_id'] not in file_id_list:
                    file_id_list.append(rec['file_id'])
        return file_id_list

    def delete_not_nse_file(self):
        """
        执行删除文件表操作
        """
        file_id_list = self.get_file_id_list()
        for file_id in file_id_list:
            self.env['file.library'].sudo().browse(int(file_id)).unlink()

    @api.model
    def backup_file(self):
        """
        备份文件/并且删除没使用的文件

        """
        date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        target_ir = TARGET_DIR + r'\%s' % date_time
        self.zip(BACKUP_FOLDER, target_ir + '.zip')
        data = {
            'name': date_time,
            'backup_file_path': target_ir + '.zip'
        }
        self.with_user(self.env.uid).create(data)
        self.delete_not_nse_file()

    @staticmethod
    def zip(dirname, zipfile_name):
        """
        将目标文件夹打包压缩

        :param dirname: 需要压缩的文件
        :param zipfile_name: 压缩后的文件名称
        """
        filelist = []
        if os.path.isfile(dirname):
            filelist.append(dirname)
        else:
            for root, dirs, files in os.walk(dirname, topdown=False):
                if not files and not dirs:
                    filelist.append(root)
                for name in files:
                    filelist.append(os.path.join(root, name))
        zf = zipfile.ZipFile(zipfile_name, "w", zipfile.ZIP_DEFLATED)
        for tar in filelist:
            arcname = tar[len(dirname):]
            zf.write(tar, arcname)
        zf.close()


