import datetime
import json
import os
import shutil
import subprocess
import threading
import zipfile
import requests
import dtcloud

from dtcloud import http
from utils.log.logger import output_log
from base_addons.common.api_parse_sdb.parse_sdb import ParseSdb
from base_addons.common.redis.redis_queue import RedisQueue
from dtcloud.addons.web.controllers.main import Home

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

REVIT_EXE = dtcloud.tools.config.get('revit_exe')
DGN_EXE = dtcloud.tools.config.get('dgn_exe')
NAVISWORKS_EXE = dtcloud.tools.config.get('navisworks_exe')


class ModelFormatConvert(Home):

    @staticmethod
    def _call_exe_option(ext: str) -> str:
        """
        调用exe的选择

        :param ext: 文件格式
        :return: 调用exe地址
        """
        revit_exe = dtcloud.tools.config.get('revit_exe')
        dgn_exe = dtcloud.tools.config.get('dgn_exe')
        navisworks_exe = dtcloud.tools.config.get('navisworks_exe')
        if ext in ['rvt', 'rfa', 'rte']:
            exe_path = revit_exe
        elif ext == 'dgn':
            exe_path = dgn_exe
        else:
            exe_path = navisworks_exe
        return exe_path

    @staticmethod
    def _generate_features(visual_style: str, exclude_lines: bool, exclude_points: bool, use_google_draco: bool,
                           extract_shell: bool, generate_models_db: bool, generate_thumbnail: bool,
                           enable_automatic_split: bool, allow_regroup_nodes: bool) -> str:
        """
        转换特性生成

        :param visual_style: 视觉样式
        :param exclude_lines: 模型线
        :param exclude_points: 模型点
        :param use_google_draco: 应用Google_Draco压缩数据（速度较慢）
        :param extract_shell: 提取输出建筑外壳（速度较慢）
        :param generate_models_db: 生成属性数据库（*.sdb by SQLite）
        :param generate_thumbnail: 生成缩略图
        :param enable_automatic_split: 自动拆分整个模型为较小的分片（大幅提升加载性能，大模型建议勾选）
        :param allow_regroup_nodes: 优化节点（glTF node）层级
        :return: features
        """
        visual_style_dict = {
            'Textured': 'UseBasicRenderColor',  # 纹理
            'Wireframe': 'ExcludeTexture,Wireframe',  # 线框
            'Gray': 'ExcludeTexture,Gray',  # 灰模
            'Colored': 'ExcludeTexture,UseViewOverrideGraphic',  # 着色
            'Realistic': '',  # 真实
        }  # 视觉样式
        features = visual_style_dict[visual_style]  # --features
        # 排除 模型线
        if exclude_lines:
            features = features + ',ExcludeLines' if features else features + 'ExcludeLines'
        # 排除 模型点
        if exclude_points:
            features = features + ',ExcludePoints' if features else features + 'ExcludePoints'
        # 勾选 应用Google_Draco压缩数据（速度较慢）
        if use_google_draco:
            features = features + ',UseGoogleDraco' if features else features + 'UseGoogleDraco'
        # 勾选 提取输出建筑外壳（速度较慢）
        if extract_shell:
            features = features + ',ExtractShell' if features else features + 'ExtractShell'
        # 勾选 生成属性数据库（*.sdb by SQLite）
        if generate_models_db:
            features = features + ',GenerateModelsDb' if features else features + 'GenerateModelsDb'
        # 勾选 生成缩略图
        if generate_thumbnail:
            features = features + ',GenerateThumbnail' if features else features + 'GenerateThumbnail'
        # 勾选 自动拆分整个模型为较小的分片（大幅提升加载性能，大模型建议勾选）
        if enable_automatic_split:
            features = features + ',EnableAutomaticSplit' if features else features + 'EnableAutomaticSplit'
        # 勾选 优化节点（glTF node）层级
        if allow_regroup_nodes:
            features = features + ',AllowRegroupNodes' if features else features + 'AllowRegroupNodes'
        if features:
            features = '--features ' + features  # --features
        return features

    @classmethod
    def _file_extraction(cls, file_name: str, file_out_dir: str, file_ext: str, middle_dir: str):
        """
        中间文件处理，获取需要的文件

        :param file_name: 文件名称
        :param file_out_dir: 文件保存文件夹路径
        :param file_ext: 文件后缀名
        :param middle_dir: 中间文件地址
        """
        tem_dir = cls._generate_tem_dir(file_name)
        file_out_path = cls._generate_path(file_out_dir, file_name, file_ext)
        if not os.path.exists(middle_dir):
            os.makedirs(middle_dir)
        if not os.path.exists(file_out_dir):
            os.makedirs(file_out_dir)
        for file in os.listdir(middle_dir):
            ext = file.rsplit('.')[-1]
            tem_path = tem_dir + '/' + file
            source_path = middle_dir + '/' + file
            if ext in ['gltf', 'glb', 'jpg', 'png']:
                shutil.copyfile(source_path, tem_path)
            if ext == 'sdb':
                shutil.copyfile(source_path, file_out_path.replace(file_out_path.rsplit('.', 1)[-1], 'sdb'))
                with open(tem_path.replace(f".{tem_path.rsplit('.', 1)[-1]}", '.json'), 'w', encoding='utf-8') as f:
                    json.dump(ParseSdb.parse_sdb_get_model_tree(source_path), f, indent=4, ensure_ascii=False)
        cls.zip(tem_dir, file_out_path.replace(f".{file_out_path.rsplit('.', 1)[-1]}", '.zip'))
        if os.path.exists(tem_dir):
            shutil.rmtree(tem_dir)

    @staticmethod
    def create_conversion_record(pyload_data):
        """
        创建转换记录

        :param pyload_data: 文件名称
        """
        post_data = {
            "data": json.dumps(pyload_data),
            "uid": 2,
        }
        server_url = dtcloud.tools.config.get('server_url')
        request_info = requests.post('%s/api/v1/conversion_record' % server_url, data=post_data)
        info = json.loads(request_info.text)
        return info

    @staticmethod
    def write_conversion_record(pyload_data, res_id):
        """
        创建转换记录

        :param pyload_data: 文件名称
        """
        post_data = {
            "data": json.dumps(pyload_data),
            "uid": 2,
        }
        server_url = dtcloud.tools.config.get('server_url')
        requests.put('%s/api/v1/conversion_record/%s' % (server_url, res_id), data=post_data)

    @classmethod
    def _perform_convert(cls, exe_path: str, features: str, level_of_detail: str, format: str, input: str, output: str,
                         file_name: str, file_out_dir: str, file_ext: str, middle_dir: str, kw: dict):
        """
        最终调用终端执行转换

        :param exe_path: 调用exe的地址
        :param features: 转换特性
        :param level_of_detail: 精度等级
        :param format: 转换文件格式
        :param input: 转换文件输入地址
        :param output: 转换文件输出地址
        :param file_name: 文件名
        :param file_out_dir: 文件输出文件夹路径
        :param file_ext: 文件后缀
        :param middle_dir: 转换文件输出地址
        :param kw: 接口入参
        """
        try:
            cmd = f'{exe_path} {features} {level_of_detail} {format} {input} {output}'
            subprocess.run(cmd, shell=True, check=True)
            cls._file_extraction(file_name, file_out_dir, file_ext, middle_dir)
            file_in_dir = kw.get('file_in_dir')
            is_convert = dtcloud.tools.config.get('is_convert')
            if is_convert:
                version = cls._rvt_version_check(file_in_dir, file_name, kw)
                # threading_1 = threading.Thread(target=cls._create_review_model_json,
                #                                args=(version, file_in_dir, file_out_dir, file_name))
                # threading_1.start()
                cls._create_review_model_json(version, file_in_dir, file_out_dir, file_name)
            data = {
                "result": "成功",
                'message': "转换成功，地址：%s" % output
            }
            cls.write_conversion_record(data, kw.get('record_id'))
            return True
        except Exception as e:
            output_log(str(e), "_perform_convert", kw, "rvt")
            data = {
                "result": "失败",
                'message': "失败，%s" % e
            }
            cls.write_conversion_record(data, kw.get('record_id'))
            return False

    @staticmethod
    def _generate_path(dir: str, file_name: str, file_ext: str) -> str:
        """
        生成文件保存地址，作为转换的输入地址

        :param dir: 文件夹
        :param file_name: 文件名
        :param file_ext: 文件后缀
        :return: 转换模型输入地址
        """
        complete_file_name = file_name + "." + file_ext
        complete_path = os.path.join(dir, complete_file_name)
        return complete_path

    @staticmethod
    def _generate_tem_dir(file_name: str) -> str:
        """
        生成文件保存地址，作为转换的输入地址

        :param file_name: 文件名称
        :return: 转换模型输入地址
        """
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
        tem_path = os.path.join(BASE_DIR, 'static')
        tem_path = os.path.join(tem_path, 'tem_file')
        tem_path = os.path.join(tem_path, now_time)
        tem_path = os.path.join(tem_path, file_name)
        if not os.path.exists(tem_path):
            os.makedirs(tem_path)
        return tem_path

    @staticmethod
    def zip(dirname, zipfile_name):
        """
        将目标文件夹打包压缩\n
        :param dirname: 需要压缩的文件
        :param zipfile_name: 压缩后的文件名称
        :return:
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
        return ''

    @http.route('/web/model/format/convert', type='http', auth="none", csrf=False,
                method=["POST"],
                website=True, cors="*")
    def model_format_convert_main(self, **kw):
        data = {
            'file_name': kw.get('file_name'),
            'file_ext': kw.get('file_ext'),
            'file_in_dir': kw.get('file_in_dir'),
            'file_out_dir': kw.get('file_out_dir'),
            'middle_dir': kw.get('middle_dir'),
            'conversion_type': '模型转换',
            'visual_style': kw.get('visual_style', 'Textured')
        }
        info = self.create_conversion_record(data)
        if info["message"]["flag"] == "success":
            kw['record_id'] = info["data"]
            q = RedisQueue('rq')  # 新建队列名为rq
            q.put(json.dumps(kw))
            data = {
                "errcode": 0,
                "errmsg": "ok",
                "message": '转换成功!',
            }
            return json.dumps(data)
        else:
            data = {
                "errcode": -1,
                "errmsg": "no",
                "message": '转换失败!',
            }
            return json.dumps(data)

    @http.route('/web/model/format/convert/queue', type='http', auth="none", csrf=False,
                method=["POST"],
                website=True, cors="*")
    def model_format_convert_queue(self, **kw):
        # :::::::::::接口参数
        if 'record_id' not in kw:
            data = {
                'file_name': kw.get('file_name'),
                'file_ext': kw.get('file_ext'),
                'file_in_dir': kw.get('file_in_dir'),
                'file_out_dir': kw.get('file_out_dir'),
                'middle_dir': kw.get('middle_dir'),
                'conversion_type': '模型转换',
                'visual_style': kw.get('visual_style', 'Textured')
            }
            info = self.create_conversion_record(data)
            if info["message"]["flag"] == "success":
                kw['record_id'] = info["data"]
        file_name = kw.get('file_name')
        file_ext = kw.get('file_ext')
        file_in_dir = kw.get('file_in_dir')  # 输入路径
        file_out_dir = kw.get('file_out_dir')  # 输出路径
        middle_dir = kw.get('middle_dir')  # 中间文件路径
        # 【基本--视觉样式（Textured:纹理,Wireframe:线框,Gray:灰模,Colored:着色,Realistic:真实）,默认Colored】
        visual_style = kw.get('visual_style', 'Textured')
        exclude_lines = kw.get('exclude_lines', True)  # 是否勾选【排除--模型线】
        exclude_points = kw.get('exclude_points', True)  # 是否勾选【排除--模型点】
        use_google_draco = kw.get('use_google_draco', False)  # 是否勾选【高级--应用Google_Draco压缩数据（速度较慢）】
        extract_shell = kw.get('extract_shell', False)  # 是否勾选【高级--提取输出建筑外壳（速度较慢）】
        generate_models_db = kw.get('generate_models_db', True)  # 是否勾选【高级--生成属性数据库（*.sdb by SQLite）】
        generate_thumbnail = kw.get('generate_thumbnail', False)  # 是否勾选【高级--生成缩略图】
        # 是否勾选【高级--自动拆分整个模型为较小的分片（大幅提升加载性能，大模型建议勾选）】
        enable_automatic_split = kw.get('enable_automatic_split', True)
        allow_regroup_nodes = kw.get('allow_regroup_nodes', False)  # 是否勾选【高级--优化节点（glTF node）层级】
        level_of_detail = kw.get('level_of_detail', '6')  # 【基本--详细程度（rvt:[0~15],）】
        format = kw.get('format', 'glb')  # gltf/glb

        # ::::::::::::转换参数生成
        # 调用exe
        exe_path = self._call_exe_option(file_ext)  # 获取转换调用exe的地址
        # 转换输入路径
        input_path = self._generate_path(file_in_dir, file_name, file_ext)
        input = f'--input "{input_path}"'  # 文件输入地址
        # 转换后输出路径
        output_path = self._generate_path(middle_dir, file_name, format)
        output = f'--output  "{output_path}"'  # 文件输出地址
        # 转换格式
        format = '--format ' + 'gltf'
        # 精度等级
        level_of_detail = '--levelofdetail ' + level_of_detail
        # 转换特性
        features = self._generate_features(visual_style, exclude_lines, exclude_points, use_google_draco, extract_shell,
                                           generate_models_db, generate_thumbnail, enable_automatic_split,
                                           allow_regroup_nodes)  # 转换特性
        result = self._perform_convert(exe_path, features, level_of_detail, format, input, output, file_name,
                                       file_out_dir,
                                       file_ext, middle_dir, kw)
        if result:
            preview_dir = file_out_dir.split('my_file', 1)[-1]
            file_url = dtcloud.tools.config.get('file_url')
            zip_url = f"{file_url}{preview_dir}/{file_name}.zip"
            sdb_url = f"{file_url}{preview_dir}/{file_name}.sdb"
            build_json_url = f"{file_url}{preview_dir}/build_json.zip"
            element_json_url = f"{file_url}{preview_dir}/element_json.zip"
            url = {
                'zip_url': zip_url,
                'sdb_url': sdb_url,
                'build_json_url': build_json_url,
                'element_json_url': element_json_url,
            }
            data = {
                "errcode": 0,
                "url": url,
                "message": '转换成功!',
            }
            return json.dumps(data)
        else:
            data = {
                "errcode": -1,
                "message": '转换失败-详情请看转换服务日志!',
            }
            return json.dumps(data)

    @staticmethod
    def _rvt_version_check(file_in_dir: str, file_name: str, kw: dict):
        """
        检测rvt模型的版本
        Args:
            file_in_dir: 文件地址
            file_name: 文件名称
            kw:

        Returns:

        """
        rvt_version_check_exe = os.path.join(BASE_DIR, 'static')
        rvt_version_check_exe = os.path.join(rvt_version_check_exe, 'exe')
        rvt_version_check_exe = os.path.join(rvt_version_check_exe, 'RevitVersion.exe')
        info = os.popen(r'"%s" "%s/%s.rvt"' % (rvt_version_check_exe, file_in_dir, file_name))
        for version in info:
            version = version.replace("\n", '')
            if version not in ('2016', '2017', '2018', '2019', '2020'):
                output_log('模型版本不正--' + version, "rvt_version_check_exe", kw)
                return False
            else:
                return version
        return True

    @staticmethod
    def _create_review_model_json(version: str, file_in_dir: str, file_out_dir: str, file_name: str):
        """
        创建审查json
        Args:
            version: 模型版本
            file_in_dir: 输入文件文件夹地址
            file_out_dir: 输出文件文件夹地址
            file_name: 文件名

        Returns:

        """
        rvt_dt_bim_json_exe_2016 = dtcloud.tools.config.get('rvt_dt_bim_json_exe_2016')
        rvt_dt_bim_json_exe_2017 = dtcloud.tools.config.get('rvt_dt_bim_json_exe_2017')
        rvt_dt_bim_json_exe_2018 = dtcloud.tools.config.get('rvt_dt_bim_json_exe_2018')
        rvt_dt_bim_json_exe_2019 = dtcloud.tools.config.get('rvt_dt_bim_json_exe_2019')
        rvt_dt_bim_json_exe_2020 = dtcloud.tools.config.get('rvt_dt_bim_json_exe_2020')
        rvt_element_json_exe_2016 = dtcloud.tools.config.get('rvt_element_json_exe_2016')
        rvt_element_json_exe_2017 = dtcloud.tools.config.get('rvt_element_json_exe_2017')
        rvt_element_json_exe_2018 = dtcloud.tools.config.get('rvt_element_json_exe_2018')
        rvt_element_json_exe_2019 = dtcloud.tools.config.get('rvt_element_json_exe_2019')
        rvt_element_json_exe_2020 = dtcloud.tools.config.get('rvt_element_json_exe_2020')
        if version == '2016':
            rvt_dt_bim_json_exe = rvt_dt_bim_json_exe_2016
            rvt_element_json_exe = rvt_element_json_exe_2016
        elif version == '2017':
            rvt_dt_bim_json_exe = rvt_dt_bim_json_exe_2017
            rvt_element_json_exe = rvt_element_json_exe_2017
        elif version == '2018':
            rvt_dt_bim_json_exe = rvt_dt_bim_json_exe_2018
            rvt_element_json_exe = rvt_element_json_exe_2018
        elif version == '2019':
            rvt_dt_bim_json_exe = rvt_dt_bim_json_exe_2019
            rvt_element_json_exe = rvt_element_json_exe_2019
        elif version == '2020':
            rvt_dt_bim_json_exe = rvt_dt_bim_json_exe_2020
            rvt_element_json_exe = rvt_element_json_exe_2020
        else:
            return False
        print('\tINOF:version ' + version)
        print('\tINOF:rvt_dt_bim_json_exe ' + rvt_dt_bim_json_exe)
        print("\tINOF:file_in_dir " + file_in_dir)
        print("\tINOF:file_out_dir " + file_out_dir)
        print("\tINOF:file_name " + file_name)
        print("\tINOF:build_json.json 生成中 ")
        cmd = f'"{rvt_dt_bim_json_exe}" "{file_in_dir}/{file_name}.rvt" "{file_out_dir}" "build_json.json"'
        subprocess.run(cmd, shell=True, capture_output=False, check=True)
        print("\tINOF:build_json.json 生成成功 ")
        print("\tINOF:element_json.json 生成中 ")
        cmd = f'"{rvt_element_json_exe}" "{file_in_dir}/{file_name}.rvt" "{file_out_dir}" "element_json.json"'
        subprocess.run(cmd, shell=True, capture_output=False, check=True)
        print("\tINOF:element_json.json 生成成功 ")
        return True
