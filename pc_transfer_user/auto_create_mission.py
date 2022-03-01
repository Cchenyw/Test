import json
import sys

import requests


# 新建任务
def create_mission(mission_info, numbers, quantity=1):
    seq = int(mission_seq())
    # 保存初始任务名称
    mission_name = f"{mission_info['name']}"
    # 批量创建任务
    for index in range(int(quantity)):
        print(f'当前初始化序列值为:{seq}')
        mission_info['name'] = f"{mission_name}-{str(seq)}"
        cookies = get_cookie()
        respond = requests.post('http://call-dev4.tangees.com/api/task', data=mission_info, cookies=cookies,
                                verify=False)
        # 请求失败重试=>更新Cookies
        if respond.status_code != 200:
            update_cookie()
            cookies = get_cookie()
            respond = requests.post('http://call-dev4.tangees.com/api/task', data=mission_info, cookies=cookies,
                                    verify=False)
        if respond.status_code == 200:
            print(f'任务:{mission_info["name"]}，创建成功!')
        else:
            print(f'任务:{mission_info["name"]}，创建失败！')
            # print(respond.text)
            decode_msg(respond)  # 1008
            exit(1)
        respond_dict = json.loads(respond.text)
        add_numbers(respond_dict['task_id'], cookies, numbers)
        seq += 1
    # 保存新建任务的序列号
    mission_seq(seq)


# 添加号码
def add_numbers(task_id, cookies, numbers):
    respond = requests.put(f'http://call-dev4.tangees.com/api/task/{task_id}/numbers/add', data=numbers,
                           cookies=cookies, verify=False)
    if respond.status_code == 200:
        print('添加号码成功！')
    else:
        print('添加号码失败！')
        # print(respond.text)
        decode_msg(respond)  # 1008


# 获取cookie
def get_cookie():
    try:
        with open(f'{sys.path[0]}\\data\\cookies.txt', 'r') as f:
            cookies = json.loads(f.read())
            return cookies
    # 获取Cookies失败、Cookies过期=>更新Cookies，并重新获取
    except Exception:
        update_cookie()
        get_cookie()


# 更新cookie
def update_cookie():
    login_request = requests.post(url='http://user-dev4.tangees.com/api/individual-user/login',
                                  data={'phone': '17520544566',
                                        'password': '69b77fe60044a9706bddd58cd37373d6',
                                        'remember': 0,
                                        'code': None,
                                        'area_code': '86'}, verify=False)
    # 关键步骤，把Session记录到当前企业[机器人测试企业2]
    enter_request = requests.post('http://user-dev4.tangees.com/api/company/enter',
                                  data={'company_id': '5c4c0805931dac1830a8b30a'},
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


if __name__ == "__main__":
    transfer_user_ids = [
        # '5f913094071bac2be31d333b'  # 我
        '611ce69e071bac762ebc6fcf'  # 李锐星
        # '61149418071bac12d878af61'  # 伟柱
    ]
    info = {
        'graph_id': '5e0d9bc21ef5e0648531034c',
        'version_id': '5edb3d401ef5e00d8632e175',
        'robot_ids': '611386e6ed8713444626f4ef',
        'wechat_push_tragger': 0,
        'sms_trigger': 0,
        'num_filter_type': 0,
        'is_transfer': 1,
        'transfer_type': 1,
        'smart_schedule_trigger': 1,
        'smart_schedule_rule': 1,
        'is_timed_task': 0,
        'redial_trigger': 0,
        'call_line_model': 2,
        'call_port_ids': '6152be0bed87135abf16e578',
        'transfer_user_ids': transfer_user_ids,
        'name': '1011星哥专用转人工'
    }
    # 伟柱电话 13826489242
    number_dict = {
        'contact_datas': '[{"number": "13827704935", "vars": {}}]'  # 李锐星
        # 'contact_datas': '[{"number": "18027464014", "vars": {}}]',  # 我
        # 'contact_datas': '[{"number": "13826489242", "vars": {}}]'  # 伟柱
    }
    # 新建任务成功
    # 新建任务失败=>重新获取Cookie=>保存到本地
    # info = {
    #     'graph_id': '613f19b2ed871374039923c1',
    #     'version_id': '613f19b2ed871374039923c2',
    #     'robot_ids': '611386e6ed8713444626f4ef',
    #     'wechat_push_tragger': 0,
    #     'sms_trigger': 0,
    #     'num_filter_type': 0,
    #     'is_transfer': 1,
    #     'transfer_type': 1,
    #     'smart_schedule_trigger': 1,
    #     'smart_schedule_rule': 1,
    #     'is_timed_task': 0,
    #     'redial_trigger': 0,
    #     'call_line_model': 2,
    #     'call_port_ids': '614d3308ed87131c3c2c25a9,614d3253ed87131c3c2c2584',
    #     'transfer_user_ids': '6100f31b071bac6feb0a7ea1,60ee4810071bac03d08092d2',
    #     'name': '测试转人工'
    # }
    # number_dict = {
    #     'contact_datas': '[{"number": "18218644344", "vars": {}}]'
    # }
    # mission_info 任务信息
    # numbers 号码信息
    # quantity 生成任务数
    create_mission(mission_info=info, numbers=number_dict, quantity=20)
