# 新城建转换服务

### 介绍

服务于文件服务，为其提供转换服务，用于生成预览调用的可用文件。  
支持转换格式：doc、docx、xls、ppt、txt、rvt、xlsx、pptx、3dm、3ds、3dxml、asm、catpart、
catproduct、dae、dgn、dwf、dwfx、dwg、dxf、fbx、gbg、gbq、gcl、gdq、ggj、
gjg、gmp、gpb、gpv、gqi、gsc、gsh、gtb、gtj、gzb、iam、ifc、igms、ipt、jt、nwc、nwd、obj、osgb、ply、prt、rfa、rte、rvm、rvt、shp、skp、sldasm、
sldprt、step、stl、stp等多种格式。

### 接口
接口地址：https://console-docs.apipost.cn/preview/4a852d56f58fa58f/d9d31ab0eeee68f2
> /web/document/libre/convert

概要：普通文档调用该接口转换。  
参数：ext&emsp;文件后缀名称  
&emsp;&emsp;&emsp;file_path&emsp;文件完整路径  
&emsp;&emsp;&emsp;file_out_dir&emsp;文件输出文件夹地址
> /web/document/office/convert

概要：特殊word调用该接口转换。  
参数：file_path&emsp;文件输入完整路径  
&emsp;&emsp;&emsp;file_out_path&emsp;文件输出完整路径

> /web/dwg/convert

概要：dwg图纸调用该接口转换。  
参数：file_dwg_dir&emsp;dwg文件夹地址  
&emsp;&emsp;&emsp;file_out_path&emsp;转换后dxf文件夹地址

> /web/model/format/convert

概要：bim模型调用该接口转换。  
参数：file_name&emsp;文件名称（不带后缀）  
&emsp;&emsp;&emsp;file_ext&emsp;文件后缀名称  
&emsp;&emsp;&emsp;file_in_dir&emsp;输入文件夹地址   
&emsp;&emsp;&emsp;file_out_dir&emsp;输出文件夹地址  
&emsp;&emsp;&emsp;middle_dir&emsp;中间文件文件夹地址   
&emsp;&emsp;&emsp;visual_style&emsp;【视觉样式】（Textured:纹理,Wireframe:线框,Gray:灰模,Colored:着色,Realistic:真实）,默认Colored   
&emsp;&emsp;&emsp;exclude_lines&emsp;是否勾选【模型线】，默认true，勾选   
&emsp;&emsp;&emsp;exclude_points&emsp;是否勾选【模型点】，默认true，勾选  
&emsp;&emsp;&emsp;use_google_draco&emsp;是否勾选【应用Google_Draco压缩数据（速度较慢）,默认false，不勾选   
&emsp;&emsp;&emsp;extract_shell&emsp;是否勾选【提取输出建筑外壳（速度较慢）】,默认false，不勾选   
&emsp;&emsp;&emsp;generate_models_db&emsp;是否勾选【生成属性数据库（*.sdb by SQLite）】，默认true，勾选  
&emsp;&emsp;&emsp;generate_thumbnail&emsp;是否勾选【生成缩略图】,默认false，不勾选  
&emsp;&emsp;&emsp;enable_automatic_split&emsp;# 是否勾选【自动拆分整个模型为较小的分片（大幅提升加载性能，大模型建议勾选）】,默认false，不勾选   
&emsp;&emsp;&emsp;allow_regroup_nodes&emsp;是否勾选【优化节点（glTF node）层级】,默认false，不勾选   
&emsp;&emsp;&emsp;level_of_detail&emsp;详细程度,默认6   
&emsp;&emsp;&emsp;format&emsp;转换后格式（gltf/glb），默认glb

### config配置

> 特殊配置的参数  
> &emsp;1. dwg2dxf_exe_path： dwg转dxf的调用exe路径  
> &emsp;&emsp;exe下载地址:https://gitee.com/new-urban-construction/dwg-dxf.git  ，下载后需安装  
> &emsp;2. libre_office_path:普通文档转换调用exe路径  
> &emsp;&emsp;exe下载地址:https://gitee.com/open_product/libreoffice.git  ，下载即可食用  
> &emsp;3. log_file_rvt:模型转换错误日志  
> &emsp;4. log_file_dwg:dwg图纸转换错误日志   
> &emsp;5. log_file_document_libre:普通文档转换错误日志   
> &emsp;6. log_file_document_office:特殊word转换错误日志  
> &emsp;7. revit_exe:rvt、rfa、rte模型调用的exe安装地址  
> &emsp;8. dgn_exe:dgn模型调用的exe安装地址  
> &emsp;9. navisworks_exe:其他模型调用的exe安装地址    
> &emsp;10. server_url:当前转换服务地址（有外网地址用外网地址）

### 安装教程

1、配置虚拟环境  
File->Settings->Project->Python Interpreter 追加虚拟路径  

2、Edit configuration 中配置  
&emsp;&nbsp;Script path：项目的bin路径。示例:D:\a_file_convert\file-conversion\dtcloud-bin  
&emsp;&nbsp;Parameter：执行conf 数据库设定  
&emsp;&nbsp;Python Interpreter ： 选择上面配置的虚拟路径  

3、Terminal中执行：pip install -r requirements.txt -i https://pypi.douban.com/simple/  

4、如果需要加入单个的包，执行：pip install 包名  
&emsp;&nbsp;如果需要指定版本，执行 pip install 包名==版本号  

5、dtcloud.conf 中修改数据库的信息  

```bash
国内镜像:
https://pypi.douban.com/simple/ 豆瓣
https://mirrors.aliyun.com/pypi/simple/ 阿里
https://pypi.hustunique.com/simple/ 华中理工大学
https://pypi.sdutlinux.org/simple/ 山东理工大学
https://pypi.mirrors.ustc.edu.cn/simple/ 中国科学技术大学
https://pypi.tuna.tsinghua.edu.cn/simple 清华

引申:更新pip
python -m pip install --index-url https://pypi.douban.com/simple --upgrade pip
```
