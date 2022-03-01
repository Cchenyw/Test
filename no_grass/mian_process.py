import json
import os
import sys
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

dev = 'http://call-dev.tangees.com'
uat = 'https://call-uat.tangees.com'
user = 'https//call-uat.tangee.com'
test = 'https://call-test.tangees.com'
base_url = test

# 标注平台环境
mark_platform_env = 'test'


# 新建任务
def create_mission(info, cookies, seq):
    # 保存初始任务名称
    mission_name = f"{info['name']}"
    # 创建任务
    print(f'当前初始化序列值为:{seq}')
    info['name'] = f"{mission_name}-{str(seq)}"
    respond = requests.post(f'{base_url}/api/task', data=info, cookies=cookies,
                            verify=False)
    if respond.status_code == 200:
        print(f'任务:{info["name"]}，创建成功!')
    else:
        print(f'任务:{info["name"]}，创建失败！')
        # print(respond.text)
        decode_msg(respond)  # 1008
        exit(1)
    respond_dict = json.loads(respond.text)
    return respond_dict['task_id']


# 添加号码
def add_numbers(task_id, cookies, numbers, seq):
    increase_number = increase_seq(numbers, seq)
    respond = requests.put(f'{base_url}/api/task/{task_id}/numbers/add', data=increase_number,
                           cookies=cookies, verify=False)
    if respond.status_code == 200:
        print('添加号码成功！')
        # 还原初始数据
    else:
        print('添加号码失败！')
        # print(respond.text)
        decode_msg(respond)  # 1008


# 获取cookie
def get_cookie():
    try:
        with open(f'{sys.path[0]}' + os.sep + 'data' + os.sep + 'cookies.txt', 'r') as f:
            cookies = json.loads(f.read())
            return cookies
    # 获取Cookies失败、Cookies过期=>更新Cookies，并重新获取
    except Exception:
        update_cookie()
        get_cookie()


# 更新cookie
def update_cookie():
    login_request = requests.post(url=f'{base_url}/api/individual-user/login',
                                  data={'phone': '17520544566',
                                        'password': '69b77fe60044a9706bddd58cd37373d6',
                                        'remember': 0,
                                        'code': None,
                                        'area_code': '86'}, verify=False)
    for cookie in login_request.cookies.items():
        print(cookie)
    # 关键步骤，把Session记录到当前企业[dev2app测试企业]
    enter_request = requests.post(f'{base_url}/api/company/enter',
                                  data={'company_id': '5c3dc69b931dac56893406e7'},
                                  cookies={'accountCenterSessionId': login_request.cookies.items()[0][1]}, verify=False)
    cookies = {}
    for cookie in enter_request.cookies.items():
        # 把cookie以键值对的方式写入dict中
        cookies[cookie[0]] = cookie[1]
    cookies_json = json.dumps(cookies)
    with open(f'{sys.path[0]}\\data\\cookies.txt', 'w') as f:
        f.write(cookies_json)


# 记录和读取任务名字序列
def mission_seq(num=0):
    if num == 0:
        try:
            with open(f'{sys.path[0]}\\data\\mission_seq.txt', 'r') as f:
                return int(f.read())
        except Exception:
            return 1
    else:
        with open(f'{sys.path[0]}\\data\\mission_seq.txt', 'w') as f:
            f.write(str(num))


# 请求失败信息处理 --转码
def decode_msg(respond):
    try:
        massage = respond.json()  # dict
        massage['msg'] = massage['msg'].encode().decode()
        print(massage)
    except Exception:
        print(respond.text)

    # print(respond.text)


# 启动任务
def start_mission(task_id, cookies):
    respond = requests.put(f'{base_url}/api/tasks/start', cookies=cookies, data={
        'open_diagnosis': 0,
        'task_ids': task_id
    }, verify=False)
    if respond.status_code == 200:
        print('任务启动成功！')
    else:
        print('任务启动失败！')
        # print(respond.text)
        decode_msg(respond)  # 1008
        exit(1)


# 检查任务是否完已成
def is_finish_mission(task_id, cookies):
    flag = 1
    while flag == 1:
        respond = requests.get(f'{base_url}/api/task/{task_id}', cookies=cookies, verify=False)
        if respond.status_code == 200:
            respond_dict = respond.json()
            if respond_dict['status'] == 'finished':
                print(
                    f'任务：{respond_dict["name"]},状态：已完成，当前进度：{respond_dict["finished_count"]}/{respond_dict["total_count"]}!')
                flag = 0
            else:
                print(
                    f'任务：{respond_dict["name"]},状态：未完成,当前进度：{respond_dict["finished_count"]}/{respond_dict["total_count"]}')
                time.sleep(10)
        else:
            print('获取接口错误！')
            decode_msg(respond)
            exit(1)


# 检查通话回调（电话是否接听完毕-通话明细）-- 暂时作废，用上面的方法
# def is_finish_call(task_id, cookies):
#     flag = 1
#     call_id_list = []
#     while flag == 1:
#         respond = requests.get(
#             f'{base_url}/api/call-details?begin=0&end=50&query_type=1&task_id={task_id}',
#             cookies=cookies, verify=False)
#         if respond.status_code == 200:
#             respond_dict = respond.json()
#             total = respond_dict['total']
#             if total != 0:
#                 print(f'当前任务下，已拨打电话有{total}个')
#                 call_details = respond_dict['details']
#                 for call_detail in call_details:
#                     if call_detail['result'] == 1:
#                         call_id = call_detail['_id']
#                         call_id_list.append(call_id)
#                 # 可标注号码
#                 print(f'可标注号码共有：{len(call_id_list)}个')
#                 flag = 0
#             else:
#                 print(f'电话还未拨打完毕！当前任务id：{task_id}')
#                 decode_msg(respond)
#                 time.sleep(10)
#         else:
#             print('获取任务接口错误！')
#             decode_msg(respond)
#             exit(1)
#     return call_id_list


# get_call_id_list -- 依据判断任务已完成模块进行取数据
def get_call_id_list(task_id, cookies):
    call_id_list = []
    respond = requests.get(f'{base_url}/api/call-details?begin=0&end=50&query_type=1&task_id={task_id}',
                           cookies=cookies, verify=False)
    if respond.status_code == 200:
        respond_dict = respond.json()
        total = respond_dict['total']
        if total != 0:
            print(f'当前任务下，已拨打电话有{total}个')
            call_details = respond_dict['details']
            for call_detail in call_details:
                # 条件：接通、命中意向非空且不为其他
                if call_detail['result'] == 1:
                    if call_detail.get('intention', False) and call_detail.get('intention') != '其他':
                        call_id = call_detail['_id']
                        call_id_list.append(call_id)
                    else:
                        print(f'call_id:{call_detail["_id"]},没有命中意向或者意向为其他！')
            # 可标注号码
            print(f'可标注号码共有：{len(call_id_list)}个')
        else:
            print(f'电话号码被拦截！当前任务id：{task_id}')
            decode_msg(respond)
            exit(1)

    else:
        print('获取任务接口错误！')
        decode_msg(respond)
        exit(1)
    return call_id_list


# 循环轮询标注号码（标注平台）
def ask_mark_platform(call_id):
    flag = 1
    global mark_platform_env
    while flag == 1:
        respond = requests.put(f'http://label-{mark_platform_env}.tangees.com/api/update_call_detail', headers={
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': 'sessionId=.eJw1zjtuAzEMANG7qE5BSiJF-TIGv4gLG8HaroLcPQsEqaaY5n23ax35_GyX1_HOj3a9Rbs0zSDwLbp4AcyFYckCwCNnoREEIwyj5Tl8JIGJEdJZMlOdIYmrZIup14RKjjhH785zYFq4M9uqTWUkuJMESlfGRNPq0E7IVx53feTj9U97P_P44zGONZV8aw2TzbN37ObRfn4Brx49AA.FJsViA.LMxgPR22k29dSbDl6HbmW-33DqI; sessionId=.eJwlzjkOAjEMAMC_pKaIE598BsWOLWh3oUL8HSSaqefdbnXkeW_X5_HKS7s9dru2ZUUs3YTCh_cfa8dQR5rm3UnJXJRRJWQDzF0cHAoIXIUwanBlWRpRqqJgpVSsQqVhPAM2RCTtcMOZe_ki2jSBEleH8PaLvM48_hsGc-zEgcnYh1CVdqHRPl9u4DW8.YbmE-g.5b0E_HwVDfjPs5J3SWb3iAbJVgA; accountCenterSessionId=.eJw9jk1Lw0AQhv_LnnuY2Z3JbnoT6qVoSsFSmkvYjxnbkFRookLF_25Q8PjC-zw8X6a7FLM2zoMmJMlBi5LaRJGzU_Qlog8EoUZOqliiy6LIwTuoSMAheYnkHHirHpUTClWe44IpJBdr8ZmKlQDiGGsPJJxZEgNXOXiiUEeK1qzMVaR0U_yQbn7rSjJrjcMkK9PpTabz_3yf5PbXXGGqOdklx5UUKwgoFRblxTX9Hk7HPZ76B9u8HOZ2bIbnC0DbD-PTcdvvNo_zbvN6b-x2bMe9bfvDfQHzOV6vMizwpyTz_QNdN1Vz.FJsWhA.6ePZX_fi03lMKeq3orVTfhYIZ5Q'
        }, json={
            "call_id": call_id,
            "intention_label": 1
        })
        if respond.status_code == 200:
            flag = 0
            print(f'call_id:{call_id},已标注！')
        else:
            print('暂时找不到任务...')
            decode_msg(respond)
            time.sleep(10)
    return respond


# 预请求
def pre_request(cookies, times=3):
    for index in range(times):
        respond = requests.get(f'{base_url}/api/tasks/joined?begin=0&end=1', cookies=cookies, verify=False)
        if respond.status_code == 200:
            print('预请求成功！')
            return 'OK', cookies
        else:
            # print('预请求失败，更新cookies中...')
            # update_cookie()
            cookies = get_cookie()
    print(f'超过重试次数{times},详情请看：\n{respond.text}')
    return 'ERROR', None


# main_process_test
def main_process_test(quantity, mission_info, start_now):
    mission_info = dict(mission_info)
    # 保存最初的name
    origin_name = mission_info.get('name')
    for times in range(quantity):
        # 重置name
        mission_info['name'] = origin_name
        # 获取序列,获取cookies
        m_seq = int(mission_seq())
        # update_cookie()  # 临时
        cookies = get_cookie()
        # 预请求：检查cookies是否过期
        pre_request_status, cookies = pre_request(cookies=cookies)
        if pre_request_status == 'OK':
            # 新建任务
            task_id = create_mission(info=mission_info, cookies=cookies, seq=m_seq)
            # 更新序列
            mission_seq(m_seq + 1)
            # 添加号码
            add_numbers(task_id=task_id, cookies=cookies, numbers=number_dict, seq=m_seq)
            # 启动任务
            if start_now == 1:
                start_mission(task_id=task_id, cookies=cookies)
            # 判断任务是否完成
            is_finish_mission(task_id=task_id, cookies=cookies)
            # 通话明细获取call_id_list
            call_id_list = get_call_id_list(task_id=task_id, cookies=cookies)
            # 标注平台标注任务
            if len(call_id_list) != 0:
                for index in range(0, len(call_id_list)):
                    ask_mark_platform(call_id=call_id_list[index])
            else:
                print('无可标注号码！')


# 号码信息序列号递增
def increase_seq(numbers, seq):
    numbers_list = eval(numbers['contact_datas'])
    re_numbers_str = '['

    for index, number_info in enumerate(numbers_list):
        temp = number_info
        number_info['contact'] = f'{temp["contact"]} - {str(seq)}'
        number_info['enterprise'] = f'{temp["enterprise"]} - {str(seq)}'
        number_info = json.dumps(number_info, ensure_ascii=False)
        if len(numbers_list) - index == 1:
            re_numbers_str = re_numbers_str + str(number_info)
        else:
            re_numbers_str = re_numbers_str + str(number_info) + ','
    re_numbers_str = re_numbers_str + ']'
    # print(re_numbers_str)
    # print(numbers)
    numbers['contact_datas'] = re_numbers_str
    # print(numbers)
    return numbers


if __name__ == "__main__":
    # 我的
    m_info = {
        'graph_id': '618b68c394b3a13ac77bc2a4',
        'version_id': '619e4bc694b3a1459e0bffa8',
        'robot_ids': '6007e320e2854809335fa095',
        'wechat_push_trigger': 0,
        'sms_trigger': 0,
        'label_trigger': 1,
        'cc_assign_trigger': 1,
        'label_intentions': '1s即可,AI推荐',
        'cc_assign_strategy': 2,
        'cc_assign_ids': '618b674f97e9717f37a8be8f_467438543',
        'num_filter_type': 0,
        'is_transfer': 0,
        'smart_schedule_trigger': 1,
        'smart_schedule_rule': 1,
        'is_timed_task': 0,
        'redial_trigger': 0,
        'call_line_model': 2,
        'call_port_ids': '61934d4694b3a17b60c88506',
        'name': '消息中心测试'
    }
    number_dict = {
        'contact_datas': '[{"number": "18218644344", "contact": "小陈", "enterprise": "广州探迹科技有限公司","vars": {}}]'
    }
    # quantity 生成任务数
    q = 1
    # start_now 是否立即启动
    s_now = 1
    main_process_test(quantity=q, mission_info=m_info, start_now=s_now)
