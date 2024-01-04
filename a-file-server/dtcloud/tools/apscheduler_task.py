# pip install apscheduler

# -*- coding:utf-8 -*-


# pip install apscheduler

# -*- coding:utf-8 -*-


from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import time

sched = BlockingScheduler()
access_token = 1
uid = 0
company_id = 0


def login():
    global access_token, uid, company_id
    data = {
        'login': 'ywguser',
        'password': 'YwgUserYwgUser654321',
        'type': '0',  # 0：用帐号与密码登陆  1：手机验证码登陆  2，发送手机验证码，3：微信扫码登陆  4，APP验证码登陆
    }

    resposeReult = requests.post('http://129.204.56.200:8069/api/v1/login/0', data=data)
    try:
        result = resposeReult.json()

        if 'data' in result:
            result_data = result['data']
            access_token = result_data['access_token']
            uid = result_data['uid']
            company_id = result_data['company_id']
    except Exception as exception:
        pass


@sched.scheduled_job('interval', minutes=1)
def get_log():
    print(f' get_log @@@access_token:{access_token},uid:{uid},company_id:{company_id}')
    if uid == 0:
        login()
    data = {
        'login': 'ywgadmin',
        'password': 'ywgadminadmin123',
        "company_id": company_id,
        "function_name": '_api_dtcloud_sbomp_equipment_get_log',
        'model': 'sbomp.equipment.instance.base',
        'access_token': access_token,
        'uid': uid,
    }
    resposeReult = requests.post('http://129.204.56.200:8069/api/v1/getattr/0', data=data)
    print(f'！！！resposeReult:{resposeReult.text}')
    try:
        result = resposeReult.json()
        if 'errcode' in result:
            errcode = result['errcode']
            if str(errcode) == '401':  # 错误代码
                login()
    except Exception as exception:
        pass


if __name__ == "__main__":
    sched.start()
    sched.start()
    sched.start()
    sched.start()
    # while True:
    #     print('main-start:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #     get_log()
    #     time.sleep(20)
    #     print('main-end:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# 方式一
# def my_job():
#     print(f'{datetime.now():%H:%M:%S} Hello World ')
#
#
# sched.add_job(my_job, 'interval', seconds=5)
# sched.start()
# APScheduler 使用起来非常简单，上面的代码完成了每个五秒输出一次信息的功能，它通过如下几个步骤是实现
#
# BlockingScheduler 调度器中的一种，该种表示在进程中只运行调度程序时使用。
# sched.add_job() 添加作业，并指定调度方式为 interval，时间间隔为 5 秒
# sched.start() 开始任务

# 方式 二
# @sched.scheduled_job('interval', minutes=18)
# def my_job():
#     global access_token, uid, company_id
#
#     data = {
#         'login': 'ywguser',
#         'password': 'YwgUserYwgUser654321',
#         'type': '0',  # 0：用帐号与密码登陆  1：手机验证码登陆  2，发送手机验证码，3：微信扫码登陆  4，APP验证码登陆
#     }
#     print(f'scheduled_job data -step1:{data},access_token:{access_token}')
#     resposeReult = requests.post('http://129.204.56.200:8069/api/v1/login/0', data=data)
#     print(f'scheduled_job data:{data}\n, resposeReult:{resposeReult}')
#     try:
#         result = resposeReult.json()
#         if 'data' in result:
#             result_data = result['data']
#             access_token = result_data['access_token']
#             uid = result_data['uid']
#             company_id = result_data['company_id']
#             print(f'scheduled_job access_token:{access_token}')
#             data = {
#                 'login': 'ywgadmin',
#                 'password': 'ywgadminadmin123',
#                 "company_id": company_id,
#                 "function_name": '_api_dtcloud_sbomp_equipment_get_log',
#                 'model': 'sbomp.equipment.instance.base',
#                 'access_token': access_token,
#                 'uid': uid,
#             }
#             resposeReult = requests.post('http://129.204.56.200:8069/api/v1/getattr/0', data=data)
#         print(f'scheduled_job resposeReult:{resposeReult.text}')
#     except Exception as exception:
#         pass
#     return False
#
#
# if __name__ == "__main__":
#     sched.start()

# 如果同一个方法被添加到多个任务重，则需要指定任务 id
# @sched.scheduled_job('interval', id='my_job', seconds=5)
# @sched.scheduled_job('interval', id='my_job1', seconds=3)
# def my_job():
#     print(f'{datetime.now():%H:%M:%S} Hello World ')
# sched.start()

# 除了刚才用到的调度器，总共有如下几种
#
# BlockingScheduler 进程中只运行调度程序时使用。
# BackgroundScheduler 当没有使用任何框架时使用，并希望调度程序在应用程序的后台运行。
# AsyncIOScheduler 当应用程序使用 asyncio 模块时使用
# GeventScheduler 当应用程序使用 gevent 时使用
# TornadoScheduler 当创建 Tornado 应用时使用
# TwistedScheduler 当创建 Twisted 应用时使用
# QtScheduler 当创建 Qt 应用时使用
# 比较常用的是前两个

# 调用方式
# add_job() 中 trigger 参数为调用方式，有 interval, day, cron 三种值

# cron
# 指定时间调度，参数如下
#
# year (int|str) – 4-digit year
# month (int|str) – month (1-12)
# day (int|str) – day of the (1-31)
# week (int|str) – ISO week (1-53)
# day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
# hour (int|str) – hour (0-23)
# minute (int|str) – minute (0-59)
# second (int|str) – second (0-59)
# start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
# end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
# timezone (datetime.tzinfo|str) – time zone to use forthe date/time calculations (defaults to scheduler timezone)
# jitter (int|None) – advance or delay the job execution by jitter seconds at most.

# 当参数指定字符串时有许多种用法，比如：
# # 当前任务会在 6、7、8、11、12 月的第三个周五的 0、1、2、3 点执行
# sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
# interval
# weeks (int) – number of weeks to wait
# days (int) – number of days to wait
# hours (int) – number of hours to wait
# minutes (int) – number of minutes to wait
# seconds (int) – number of seconds to wait
# start_date (datetime|str) – starting point for(int i = 0; i < the interval calculation
# end_date (datetime|str) – latest possible date/time to trigger on
# timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
# jitter (int|None) – advance or delay the job execution by jitter seconds at most.


#
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime
# import requests
#
# sched = BlockingScheduler()
# global access_token, uid, company_id
#
#
# # 方式一
# # def my_job():
# #     print(f'{datetime.now():%H:%M:%S} Hello World ')
# #
# #
# # sched.add_job(my_job, 'interval', seconds=5)
# # sched.start()
# # APScheduler 使用起来非常简单，上面的代码完成了每个五秒输出一次信息的功能，它通过如下几个步骤是实现
# #
# # BlockingScheduler 调度器中的一种，该种表示在进程中只运行调度程序时使用。
# # sched.add_job() 添加作业，并指定调度方式为 interval，时间间隔为 5 秒
# # sched.start() 开始任务
#
# # 方式 二
# @sched.scheduled_job('interval', minutes=18)
# def my_job():
#     global access_token, uid, company_id
#
#     data = {
#         'login': 'ywguser',
#         'password': 'YwgUserYwgUser654321',
#         'type': '0',  # 0：用帐号与密码登陆  1：手机验证码登陆  2，发送手机验证码，3：微信扫码登陆  4，APP验证码登陆
#     }
#     print(f'scheduled_job data -step1:{data},access_token:{access_token}')
#     resposeReult = requests.post('http://129.204.56.200:8069/api/v1/login/0', data=data)
#     print(f'scheduled_job data:{data}\n, resposeReult:{resposeReult}')
#     try:
#         result = resposeReult.json()
#         if 'data' in result:
#             result_data = result['data']
#             access_token = result_data['access_token']
#             uid = result_data['uid']
#             company_id = result_data['company_id']
#             print(f'scheduled_job access_token:{access_token}')
#             data = {
#                 'login': 'ywgadmin',
#                 'password': 'ywgadminadmin123',
#                 "company_id": company_id,
#                 "function_name": '_api_dtcloud_sbomp_equipment_get_log',
#                 'model': 'sbomp.equipment.instance.base',
#                 'access_token': access_token,
#                 'uid': uid,
#             }
#             resposeReult = requests.post('http://129.204.56.200:8069/api/v1/getattr/0', data=data)
#         print(f'scheduled_job resposeReult:{resposeReult.text}')
#     except Exception as exception:
#         pass
#     return False
#
#
# if __name__ == "__main__":
#     sched.start()

# 如果同一个方法被添加到多个任务重，则需要指定任务 id
# @sched.scheduled_job('interval', id='my_job', seconds=5)
# @sched.scheduled_job('interval', id='my_job1', seconds=3)
# def my_job():
#     print(f'{datetime.now():%H:%M:%S} Hello World ')
# sched.start()

# 除了刚才用到的调度器，总共有如下几种
#
# BlockingScheduler 进程中只运行调度程序时使用。
# BackgroundScheduler 当没有使用任何框架时使用，并希望调度程序在应用程序的后台运行。
# AsyncIOScheduler 当应用程序使用 asyncio 模块时使用
# GeventScheduler 当应用程序使用 gevent 时使用
# TornadoScheduler 当创建 Tornado 应用时使用
# TwistedScheduler 当创建 Twisted 应用时使用
# QtScheduler 当创建 Qt 应用时使用
# 比较常用的是前两个

# 调用方式
# add_job() 中 trigger 参数为调用方式，有 interval, day, cron 三种值

# cron
# 指定时间调度，参数如下
#
# year (int|str) – 4-digit year
# month (int|str) – month (1-12)
# day (int|str) – day of the (1-31)
# week (int|str) – ISO week (1-53)
# day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
# hour (int|str) – hour (0-23)
# minute (int|str) – minute (0-59)
# second (int|str) – second (0-59)
# start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
# end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
# timezone (datetime.tzinfo|str) – time zone to use forthe date/time calculations (defaults to scheduler timezone)
# jitter (int|None) – advance or delay the job execution by jitter seconds at most.

# 当参数指定字符串时有许多种用法，比如：
# # 当前任务会在 6、7、8、11、12 月的第三个周五的 0、1、2、3 点执行
# sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
# interval
# weeks (int) – number of weeks to wait
# days (int) – number of days to wait
# hours (int) – number of hours to wait
# minutes (int) – number of minutes to wait
# seconds (int) – number of seconds to wait
# start_date (datetime|str) – starting point for(int i = 0; i < the interval calculation
# end_date (datetime|str) – latest possible date/time to trigger on
# timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations
# jitter (int|None) – advance or delay the job execution by jitter seconds at most.
