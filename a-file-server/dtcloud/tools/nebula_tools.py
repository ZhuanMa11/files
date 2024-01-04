import random
import socket
import struct
import re
import uuid
from datetime import datetime, timedelta
import pytz
import unittest

from dtcloud.tools import config
from .nebula_sql_base import get_select_sql_base, get_update_sql_base, get_insert_sql_base
from .nebula_sql_lite_tools import nebula_select_sql_lite, nebula_update_sql_lite, nebula_create_sql_lite


def get_location_time(self=False, add_hours=0,
                      add_days=0, add_minutes=0):  # 获取当前客户日期 from ...tools.nebula_tools import get_location_time
    """     获取当前时区时间(带时区)     :return:     """
    time_zone = config.get('def_time_zone', 'Asia/Shanghai')
    try:
        now_time = datetime.now(tz=pytz.timezone(time_zone))
    except:
        if self:
            tz = self.env.user.tz or 'Asia/Shanghai'
        else:
            tz = 'Asia/Shanghai'
        now_time = datetime.now(tz=pytz.timezone(tz))
    if add_hours != 0:
        now_time = now_time + timedelta(hours=add_hours)
    if add_days != 0:
        now_time = now_time + timedelta(days=add_days)
    if add_minutes != 0:
        now_time = now_time + timedelta(minutes=add_minutes)
    return now_time


def check_table_sbomp_test_ip():
    sql_text = '''CREATE TABLE IF NOT EXISTS sbomp_test_ip
               (id integer primary key  autoincrement  not null,
                ip_address varchar ,
                port varchar,
                connect_datetime DATETIME  NOT NULL,                
                reconnect_datetime DATETIME NOT NULL,
                connect_state BOOLEAN         NOT NULL);'''

    re, info = nebula_create_sql_lite(db_name='sbomp.db', create_sql=sql_text)
    if re:
        print('建表成功或表已经存在！')
    else:
        print(f'建表失败{info}')


def net_is_used(in_ip='127.0.0.1', in_port=503):
    ip = in_ip
    table_name = 'sbomp_test_ip'
    db_name = 'sbomp.db'
    connect_datetime = get_location_time()
    reconnect_datetime = get_location_time(add_minutes=10)
    # 如果传进来的是  '192.168.3.3:503'
    ip_port_list = in_ip.split(':')
    if len(ip_port_list) == 2:
        # print(f'ip_port_list:{ip_port_list} in_ip:{in_ip}')
        ip_tmp = ip_port_list[0]
        ip = ip_tmp.replace('\'', '')
        port_tmp = ip_port_list[1]
        port = port_tmp.replace('\'', '')
        # print(f'ip_port_list ip_port_list :{ip_port_list} in_ip:{in_ip}, ip:{ip},port:{port}')
        port = int(port)
    else:  # 如果传进来的端口是字符
        if type(in_port) == str:
            port = int(in_port)
        else:
            port = in_port

    # 测试本地IP是否正常
    # 先查看有没有这条记录
    ip_address = str(ip)
    str_port = str(port)

    where_values = 'ip_address=? and port=?'
    in_parameters = (ip_address, str_port)
    check_table_sbomp_test_ip()
    select_sql = get_select_sql_base(table_name=table_name, select_values='id,connect_state,reconnect_datetime',
                                     where_values=where_values)
    re_state, db_list = nebula_select_sql_lite(select_sql, db_name=db_name, in_parameters=in_parameters)
    if re_state:  # 有返回值,正常
        for db_one in db_list:  # 如果是断开状态，而且日期是小于重新检查时间，则直接返回False
            s_none_format = "%Y-%m-%d %H:%M:%S"
            db_one_connect_state = bool(db_one[1])
            db_one_reconnect_datetime_str = db_one[
                2]  # 2021-03-17 03:10:42.817235+08:00' does not match format '%Y-%m-%d %H:%M:%S.%f%z'

            s_tz = db_one_reconnect_datetime_str.split('+')[1]
            s_format = s_none_format + '.%f+' + s_tz
            db_one_reconnect_datetime = datetime.strptime(db_one_reconnect_datetime_str, s_format)

            # db_one_reconnect_datetime = datetime.strptime(db_one_reconnect_datetime_str,
            #                                               "%Y-%m-%d %H:%M:%S.%f%z")  # "%Y-%m-%d %H:%M:%S.%f%z    Y-%m-%dT%H:%M:%S.%f

            # print(f'db_one_reconnect_datetime:')

            db_one_reconnect_datetime = datetime.strptime(db_one_reconnect_datetime.strftime(s_none_format),
                                                          s_none_format)

            connect_datetime = datetime.strptime(connect_datetime.strftime(s_none_format), s_none_format)

            if (not db_one_connect_state) and (connect_datetime <= db_one_reconnect_datetime):
                d_temp = db_one_reconnect_datetime - connect_datetime
                print(f'net_is_used 离下次检查时间还有{d_temp}')
                return False

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(1)
        print('net_is_used %s:%d is used' % (ip, port))
        return True
    except Exception as e:
        print(f'net_is_used 目标地址:{ip},目标端口:{port}出错，出错信息:{e}')
        connect_state = False
        if re_state:
            if len(db_list):  # 如果有返回值,更新数据
                set_values = 'connect_datetime=?,reconnect_datetime=?,connect_state=?'
                update_sql = get_update_sql_base(table_name=table_name, set_values=set_values,
                                                 where_values=where_values)
                in_parameters = (connect_datetime, reconnect_datetime, connect_state, ip_address, str_port)
                re_state, re_info = nebula_update_sql_lite(update_sql, db_name=db_name, in_parameters=in_parameters)
            else:  # 是新记录，需要插入
                set_parameters = 'ip_address,port,connect_datetime,reconnect_datetime,connect_state'
                insert_sql = get_insert_sql_base(table_name=table_name, set_parameters=set_parameters)
                in_parameters = (ip_address, str_port, connect_datetime, reconnect_datetime, connect_state)
                re_state, re_info = nebula_update_sql_lite(update_sql=insert_sql, db_name=db_name,
                                                           in_parameters=in_parameters)
            print(f'net_is_used re_state:{re_state}, db_list:{db_list}')
        return False

        # if subprocess.call(["ping", "-c", "2", ip]) == 0:  # 只发送两个echo_request包
        #     return True
        # else:
        #     return False
        # return1 = os.system('ping -n 2 -w 1 %s' % ip)  # 每个IPping2次，等待时间1s. 如果ping值=0,表示ping通
        # print(f'目标地址:{ip},目标端口:{port}出错，出错信息:{e},ping结果:{return1}')
        # if return1 == 0:
        #     return True
        # else:
        #     return False


def get_report_day_by_time(in_time_str):  # YYYY-MM-DD HH:MM:SS
    report_year = False
    report_month = False
    report_day = False
    report_hour = False
    if len(in_time_str) > 18:
        time_list = re.split(r";|-|:|\s", in_time_str)  # 分解年月日
        # print(time_list)
        zero_str = 'YYYY-00-00-00 '  # 必须有个空格，以方便切割
        num = 4  # 年报表
        report_year = time_list[0] + zero_str[num:-1]

        num = num + 3  # 月报表
        report_month = time_list[0] + '-' + time_list[1] + zero_str[num:-1]
        num = num + 3  # 日报表
        report_day = time_list[0] + '-' + time_list[1] + '-' + time_list[2] + zero_str[num:-1]
        num = num + 3  # 时报表
        report_hour = time_list[0] + '-' + time_list[1] + '-' + time_list[2] + '-' + time_list[3] + zero_str[num:-1]
    return report_year, report_month, report_day, report_hour


def _parse_with_amc72(in_list):
    Pfa = get_value_by_uint16(in_list[0], in_list[1])  # 功率因数 Pfa
    Pfb = get_value_by_uint16(in_list[2], in_list[3])
    Pfc = get_value_by_uint16(in_list[4], in_list[5])  #
    Pf = get_value_by_uint16(in_list[6], in_list[7])  # 总功率因数
    Fr = get_value_by_uint16(in_list[8], in_list[9])  # 频率
    UA = get_value_by_uint16(in_list[10], in_list[11])  # 无符号16位 uint16  相电压
    UB = get_value_by_uint16(in_list[12], in_list[13])
    UC = get_value_by_uint16(in_list[14], in_list[15])

    Uab = get_value_by_uint16(in_list[16], in_list[17])  # 无符号16位 uint16  线电压
    Ubc = get_value_by_uint16(in_list[18], in_list[19])
    Uca = get_value_by_uint16(in_list[20], in_list[21])

    Ia = get_value_by_uint16(in_list[22], in_list[23])  # 电流
    Ib = get_value_by_uint16(in_list[24], in_list[25])
    Ic = get_value_by_uint16(in_list[26], in_list[27])

    Pa = get_value_by_uint16(in_list[28], in_list[29])  # 有功功率
    Pb = get_value_by_uint16(in_list[30], in_list[31])
    Pc = get_value_by_uint16(in_list[32], in_list[33])

    P = get_value_by_uint16(in_list[34], in_list[35])

    Qa = get_value_by_uint16(in_list[36], in_list[37])  # 无功功率
    Qb = get_value_by_uint16(in_list[38], in_list[39])
    Qc = get_value_by_uint16(in_list[40], in_list[41])

    Q = get_value_by_uint16(in_list[42], in_list[43])

    Sa = get_value_by_uint16(in_list[44], in_list[45])  # 视在功率
    Sb = get_value_by_uint16(in_list[46], in_list[47])
    Sc = get_value_by_uint16(in_list[48], in_list[49])

    S = get_value_by_uint16(in_list[50], in_list[51])
    EPI = get_value_by_uint16(in_list[52], in_list[53])  # 吸收/输入有功电能
    EPE = get_value_by_uint16(in_list[54], in_list[55])  # 释放/输出有功电能
    EQL = get_value_by_uint16(in_list[56], in_list[57])  # 感性无功电能
    EQC = get_value_by_uint16(in_list[58], in_list[59])  # 容性无功电能

    print(
        f'线电压Uab:{Uab}，线电压Ubc:{Ubc},线电压Uca:{Uca},电流Ia:{Ia}，电流Ib:{Ib},电流Ic:{Ic},吸收/输入有功电能EPI(kwh):{EPI}，释放/输出有功电能EPE:{EPE}')
    # print(f'功率因数Pfa:{Pfa}，功率因数Pfb:{Pfb},功率因数Pfc:{Pfc}')
    # print(f'总功率因数Pf:{Pf}，频率Fr:{Fr}')
    # print(f'相电压UA:{UA}，相电压UB:{UB},相电压UC:{UC}')
    # print(f'线电压Uab:{Uab}，线电压Ubc:{Ubc},线电压Uca:{Uca}')
    # print(f'电流Ia:{Ia}，电流Ib:{Ib},电流Ic:{Ic}')
    # print(f'有功功率Pa:{Pa}，有功功率Pb:{Pb},有功功率Pc:{Pc}')
    # print(f'无功功率Qa:{Qa}，无功功率Qb:{Qb},无功功率Qc:{Qc}')
    # print(f'视在功率Sa:{Sa}，视在功率Sb:{Sb},视在功率Sc:{Sc}')
    # print(f'吸收/输入有功电能EPI(kwh):{EPI}，释放/输出有功电能EPE:{EPE}')
    # print(f'吸收/输入有功电能EQL:{EQL}，释放/输出有功电能EQC:{EQC}')
    result = {
        "Pfa": Pfa,
        "Pfb": Pfb,
        "Pfc": Pfc,

        "Pf": Pf,
        "Fr": Fr,
        "UA": UA,
        "UB": UB,
        "UC": UC,
        "Uab": Uab,
        "Ubc": Ubc,
        "Uca": Uca,

        "Ia": Ia,
        "Ib": Ib,
        "Ic": Ic,

        "Pa": Pa,
        "Pb": Pb,
        "Pc": Pc,

        "Sa": Sa,
        "Qb": Qb,
        "Qc": Qc,

        "Qa": Qa,
        "Sb": Sb,
        "Sc": Pc,

        "EPI": EPI,
        "EPE": EPE,
        "EQL": EQL,
        "EQC": EQC,
    }
    return result


def get_value_by_uint16(in_high, in_low):  # 传入UINT16的高低位，返回正确的数值
    if (int(in_high) + int(in_low)) == 0:
        return 0
    # print(f' get_value_by_uint16 输入值in_high:{in_high}, in_low:{in_low}')
    if type(in_high) == int:
        in_high_16 = hex(in_high)  # 十进制转十六进制
    else:
        in_high_16 = hex(int(in_high))
    if in_high_16 == '0x0':
        in_high_16 = '0x0000'  # 不足五位补零

    if in_low == 0:
        in_low_16 = '0x0000'
    else:
        in_low_16 = hex(in_low)

    # 取消 0x,然后补足0到4位
    in_low_16 = in_low_16.replace('0x', '')
    in_low_16 = in_low_16.rjust(4, '0')  # 应该右对齐，否则出错
    out_16_str = in_high_16 + in_low_16
    out_16_str = out_16_str.replace('0x', '')  # 替换掉0x
    result = struct.unpack('!f', bytes.fromhex(out_16_str))[0]
    return round(result, 1)


def get_value_by_int(in_high, in_low):  # 传入UINT16的高低位，返回正确的数值
    if (int(in_high) + int(in_low)) == 0:  # 应该是:18775 90016  传入: 28649 49152(无符号整形、两个值)
        return 0
    # print(f' get_value_by_uint16 输入值in_high:{in_high}, in_low:{in_low}')
    if type(in_high) == int:
        in_high_16 = hex(in_high)  # 十进制转十六进制 0x6ff6
    else:
        in_high_16 = hex(int(in_high))
    if in_high_16 == '0x0':
        in_high_16 = '0x0000'  # 不足五位补零

    if in_low == 0:
        in_low_16 = '0x0000'
    else:
        in_low_16 = hex(in_low)  # 0x9100

    # 取消 0x,然后补足0到4位
    in_low_16 = in_low_16.replace('0x', '')
    in_low_16 = in_low_16.rjust(4, '0')  # 应该右对齐，否则出错
    out_16_str = in_high_16 + in_low_16
    out_16_str = out_16_str.replace('0x', '')  # 替换掉0x   '0x6fe9c000' 转换成整数
    data = int(out_16_str, 16)
    return data


def change_hex(in_d):
    if type(in_d) == int:
        in_d1_16 = hex(in_d)  # 十进制转十六进制 0x6ff6
    else:
        in_d1_16 = hex(int(in_d))
    if in_d1_16 == '0x0':
        in_d1_16 = '0x0000'  # 不足五位补零
    return in_d1_16


def cut_x(in_str):  # 替换掉0x
    in_str = in_str.replace('0x', '')
    in_str = in_str.rjust(4, '0')  # 应该右对齐，否则出错
    return in_str


def get_value_by_D_ACEG(in_value):  # 传入Double AB CD EF GH，返回正确的数值
    d1 = in_value[0]
    d2 = in_value[1]
    d3 = in_value[2]
    d4 = in_value[3]
    if (int(d1) + int(d2) + int(d3) + int(d4)) == 0:
        return 0

    in_d1_16 = change_hex(d1)
    in_d2_16 = change_hex(d2)
    in_d3_16 = change_hex(d3)
    in_d4_16 = change_hex(d4)
    out_16_str = cut_x(in_d1_16) + cut_x(in_d2_16) + cut_x(in_d3_16) + cut_x(in_d4_16)
    data = struct.unpack('!d', bytes.fromhex(out_16_str))[0]  # double
    result = {
        "data": data,
    }
    return result


class UCTestCase(unittest.TestCase):
    def testCreateFolder(self):
        # uTmp = get_value_by_int(10982, 43648)
        # assert uTmp == 719760000
        # uTmp = get_value_by_int(0, 4000)
        # assert uTmp == 4000
        uTmp = get_value_by_D_ACEG(16472, 42434, 36700, 10486)
        assert uTmp == 98.59


def _parse_with_basic_csj(in_list):
    EPI = get_value_by_int(in_list[0], in_list[1])  # 吸收/输入有功电能(电表值)

    Fr = in_list[2]  # 频率

    UA = in_list[3]  # 无符号16位 uint16  相电压
    UB = in_list[4]
    UC = in_list[5]

    Ia = in_list[6]  # 电流
    Ib = in_list[7]
    Ic = in_list[8]

    Pa = in_list[9]  # 有功功率
    Pb = in_list[10]
    Pc = in_list[11]

    Pfa = in_list[12]
    Pfb = in_list[13]  #
    Pfc = in_list[14]  # 总功率因数

    print(
        f'相电压Uab:{UA}，相电压Ubc:{UB},相电压Uca:{UC},电流Ia:{Ia}，电流Ib:{Ib},电流Ic:{Ic},有功功率Pa:{Pa},有功功率Pb:{Pb},有功功率Pc:{Pc},总功率因数Pfa:{Pfa}, 总功率因数Pfb:{Pfb},总功率因数Pfa:{Pfb},吸收/输入有功电能EPI(kwh):{EPI}')

    result = {
        "EPI": EPI,

        "Fr": Fr,

        "UA": UA,
        "UB": UB,
        "UC": UC,

        "Ia": Ia,
        "Ib": Ib,
        "Ic": Ic,

        "Pa": Pa,
        "Pb": Pb,
        "Pc": Pc,

        "Pfa": Pfa,
        "Pfb": Pfb,
        "Pfc": Pfc,
    }
    return result


def parse_energy_values(in_list, protocol_type='electric_acrel_amc72'):
    result = in_list
    if type(in_list) != dict:
        if protocol_type == 'electric_acrel_amc72':
            result = _parse_with_amc72(in_list)
        elif protocol_type == 'electric_basic_csj':
            result = _parse_with_basic_csj(in_list)
    return result


def check_full_path(excel_path, file_name):  # 替换掉名字中非法的空格和冒号，返回可用的全路径
    file_new_name = file_name.replace(' ', '_')
    return excel_path + file_new_name.replace(':', '^')


def nebula_get_uuid():  # 返回UUID1和4位随机数
    return str(uuid.uuid1()) + str(random.randint(0, 10000))


def convert_number_by_char(num_char, return_decimal=False):  # 转换字符串为整形或2位小数,非正常字符串返回0,默认返回整形
    num_type = type(num_char)
    result = 0
    try:
        if num_type == str:
            if _is_number(num_char):
                if return_decimal:
                    result = round(float(num_char), 2)
                else:
                    if _is_decimal_char(num_char):  # 如果是小数，取整
                        result = int(round(float(num_char)))
                    else:
                        result = int(num_char)
        elif num_type == int:
            result = num_char
        elif num_type == float:
            if return_decimal:
                result = round(float(num_char), 2)
            else:
                result = int(round(float(num_char)))
    except  Exception as e:
        print(F'convert_number_by_char error：{e}')
    return result


def _is_decimal_char(num_char):
    num_char_new = str(num_char)
    result = False
    if num_char_new.count(".") == 1:
        left, right = num_char_new.split(".")
        if left.isdigit() and right.isdigit():
            result = True
        elif left.startswith('-') and left.count('-') == 1 and right.isdigit():
            l_left = left.split('-')[-1]
            if l_left.isdigit():
                result = True
    return result


def _is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


if __name__ == "__main__":
    unittest.main()
    # print(get_value_by_int(28649, 49152))
    # while True:
    #     try:
    #         print('setp: 1')
    #         print(net_is_used('192.168.33.242:502'))
    #     finally:
    #         print('setp: 2')
    #         print(net_is_used('192.168.33.242:502'))
    # ip_port_list: ["'192.168.3.3", "503'"]
    # in_ip: '192.168.3.3:503'
