# -*- coding: utf-8 -*-
import os.path

import requests

import dtcloud
from dtcloud import fields, models, api

MODEL_EXT = ['3dm', '3ds', '3dxml', 'asm', 'catpart', 'catproduct', 'dae', 'dgn', 'dwf', 'dwfx', 'dxf', 'fbx',
             'gbg', 'gbq', 'gcl', 'gdq', 'ggj', 'gjg', 'gmp', 'gpb', 'gpv', 'gqi', 'gsc', 'gsh', 'gtb', 'gtj', 'gzb',
             'iam', 'ifc', 'igms', 'ipt', 'jt', 'nwc', 'nwd', 'obj', 'osgb', 'ply', 'prt', 'rfa', 'rte', 'rvm', 'rvt',
             'shp', 'skp', 'sldasm', 'sldprt', 'step', 'stl', 'stp']


class ConversionRecord(models.Model):
    _name = "conversion.record"
    _description = "转换记录"
    _order = 'id desc'

    file_name = fields.Char(string="文件名称")
    file_ext = fields.Char(string="文件后缀")
    file_in_dir = fields.Char(string="转换输入文件夹")
    file_out_dir = fields.Char(string="转换输出文件夹")
    middle_dir = fields.Char(string="转换中间文件夹")
    visual_style = fields.Char(string="视觉样式")
    conversion_type = fields.Char(string="转换类型")
    result = fields.Char(string="结果")
    message = fields.Char(string="信息")

    # @api.model
    def automatically_converts_unconverted_models(self):
        records = self.env['conversion.record'].sudo().search([('file_ext', 'in', MODEL_EXT)])
        file_convert_url = dtcloud.tools.config.get('server_url')
        for rec in records:
            zip_path = f"{rec.file_out_dir}/{rec.file_name}.zip"
            if not os.path.exists(zip_path):
                post_data = {
                    "file_in_dir": rec.file_in_dir,
                    "file_out_dir": rec.file_out_dir,
                    "file_name": rec.file_name,
                    "file_ext": rec.file_ext,
                    "middle_dir": rec.middle_dir,
                }
                requests.post('%s/web/model/format/convert' % file_convert_url, data=post_data)
