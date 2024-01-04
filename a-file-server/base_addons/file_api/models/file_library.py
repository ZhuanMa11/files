# -*- coding: utf-8 -*-
# @Project  :djd_DTC
# @File     :file_library
# @Date     :2022/4/19 16:34
# @Author   :Flame!!!
# @Email    :190066183@qq.com
# @phone    :18118160329
# @Software :PyCharm

from dtcloud import fields, models
import dtcloud
import os


class FileLibrary(models.Model):
    _name = "file.library"
    _description = "系统文档"
    _order = 'id desc'

    name = fields.Char(string="名称")
    ext = fields.Char(string="扩展名")
    path = fields.Char(string="存放地址")
    size = fields.Char(string="文件大小")
    md5 = fields.Char(string="MD5文件的唯一识别key")
    view_path = fields.Char(string="预览地址")
    download_path = fields.Char(string="下载地址")

    def unlink(self):
        addons_path = dtcloud.tools.config.get('addons_path').split(',')[-1]
        if self.path:
            file_dir = os.path.join(addons_path, self.path)
            if os.path.exists(file_dir):
                try:
                    os.remove(file_dir)
                except Exception as e:
                    print(e)
            else:
                print('文件不存在')
        res = super(FileLibrary, self).unlink()
        return res

    def replace_url(self):
        """

        """
        files = self.sudo().search([])
        for rec in files:
            if rec.view_path:
                rec.view_path = rec.view_path.replace('10.201.97.20:9051', '58.240.192.243:9003')
            if rec.download_path:
                rec.download_path = rec.download_path.replace('10.201.97.20:9051', '58.240.192.243:9003')
