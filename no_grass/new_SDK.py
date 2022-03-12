import json
import time
import logging
import logging.config

import requests

import mian_process

base_url = mian_process.base_url


# 配置logging,初始化
def initial_logging():
    logging.config.fileConfig('../logging.ini')
    logger_1 = logging.getLogger('h1')
    logger_1.debug('initial debug message')
    logger_1.info('initial info message')
    logger_1.warning('initial warning message')
    logger_1.error('initial error message')
    logger_1.critical('initial critical message')


def reformat_contact_datas(contacts=[(17520544566, '公司', '联系人')]):
    contact_datas = []
    time_seq = time.strftime('%m%d%H%M%S')
    count = 0
    for contact in contacts:
        contact_data = {
            'number': str(contact[0]),
            'contact': str(contact[1]) + str(time_seq) + '-' + str(count),
            'enterprise': str(contact[2]) + str(time_seq) + '-' + str(count),
            'vars': {}
        }
        contact_datas.append(contact_data)
        count += count
        contact_data.clear()
    json_datas = json.dumps(contact_datas)
    return json_datas


def create_sdk_mission(info, contacts, cookies):
    # init
    init_mission = requests.post(f'{base_url}/api/task/init', cookies)
    try:
        task_id = init_mission.json()['task_id']
        logging.info(f'init success, task_id:%s', task_id)
    except Exception as e:
        logging.error('fail to init, error msg:%s, respond result:\n%s', e, str(init_mission.text))
        return
    # add
    numbers = reformat_contact_datas(contacts)
    numbers_dict = {
        'contact_datas': str(numbers)
    }
    add_number = requests.put(f'{base_url}/api/task/{task_id}/numbers/add', data=numbers_dict, cookies=cookies)
    if add_number.status_code == 200:
        logging.info('add number success')
        logging.debug('add number result:\n%s', str(add_number.text))
    else:
        logging.error('fail to add number, respond result:\n%s', str(add_number.text))

    # mission_setting
    mission_setting = requests.post(f'{base_url}/api/task/{task_id}/v2', data=info, cookies=cookies)
    try:
        task_status = mission_setting.json()['fail']
    except Exception as e:
        logging.error(f'setting fail, error msg:%s, respond result:\n%s', e, str(mission_setting.text))
        return
    if task_status:
        logging.debug('fail reason:%s', str(mission_setting.json()['fail_reason']))
    elif not task_status:
        logging.info('mission create success')
        return task_id
    else:
        logging.error('error, respond result:\n%s', str(mission_setting.text))


# 外呼工作台
def check_work_space(cookies, params=[1, 200]):
    # my_task
    my_task = requests.get(f'{base_url}/api/call-leads/my_task', params={
        'page': str(params[0]),
        'page_size': str(params[1])
    }, cookies={
        "accountCenterSessionId": ".eJw9jstKw1AURf_ljju479N0XCdFk4ERSSfhvG7SBxGaqFDx3w0KDjfstVhfpj-J2RkADECUiaIyI3i2XCBZyq7CjEQOlG3lMocQok1V5WIB0a1othCFKoc5ahK2PgJ7Eu8lUExbScRbC5YjhhRd4RQCopDPKwHisKxGNBszqUo_44f2y1svZHYFr7NuTF9uOo__833W219z9k7Fs2oCXyxk8up5jVxd8--hO9enpq1PdTssT_chNc_WHtvL_bEdL91rt9T7IR3bw_l4fgjN_sWtII84TXpd4U8l8_0DI11WVg.FQBoqw.9tQ3woJxLIchbtq2VSygsrzevgE"})
    print(my_task.text)
    # my_called
    my_called = requests.get(f'{base_url}/api/call-leads/my_called', params={
        'page': params[0],
        'page_size': params[1]
    }, cookies={
        "accountCenterSessionId": ".eJw9jstKw1AURf_ljju479N0XCdFk4ERSSfhvG7SBxGaqFDx3w0KDjfstVhfpj-J2RkADECUiaIyI3i2XCBZyq7CjEQOlG3lMocQok1V5WIB0a1othCFKoc5ahK2PgJ7Eu8lUExbScRbC5YjhhRd4RQCopDPKwHisKxGNBszqUo_44f2y1svZHYFr7NuTF9uOo__833W219z9k7Fs2oCXyxk8up5jVxd8--hO9enpq1PdTssT_chNc_WHtvL_bEdL91rt9T7IR3bw_l4fgjN_sWtII84TXpd4U8l8_0DI11WVg.FQBoqw.9tQ3woJxLIchbtq2VSygsrzevgE"})
    return my_task, my_called


# 检查二次推送
def check_push_mark_platform():
    mark_platform_env = mian_process.mark_platform_env
    while True:
        respond = requests.get(f'http://label-{mark_platform_env}.tangees.com/api/easy-lead/get_call_detail', headers={
            'Cookie': 'sessionId=.eJwlzkEOAjEIQNG7dO2iBQqtlzFAIbqdcVbGu9vEC_z3P-WRR5zPcn8fV9zK47XKvQgYVszB3lgHmHV16aIoOCFheNr0QQs4WYIxoQ_juRIqMxO1qRo-sC1zYVFqMXfRfNeIPT0T5nIYvCp1gN5UDSHdUcQlyx65zjj-N9yUaDtRh8e2oNWJBlS-P06NNaM.YhxoVg.x9zaEHk0IfjjxblXu5BkVMlrooI; SecurityCenterDuId=IllPYTYvSllFMjBlRWFydTlGa1VVbHBRPSI.FP8Ygg.ci1U_236EBzbyRTDHosiKunL3Vk; accountCenterSessionId=.eJw9jt1Kw0AQRt9lr3uxO_szSe-LFEyKJSjxJszszNrWJkJTLSi-u0HByw_OOXxfZjiKWRtE8sicmIPmTAjZ5oLRcnI1JWJ2qNnWLmXvfbCxrl0oKFqJJotBuHaUgkbJFgJmYAEQzyFWEjlXFm0O5GNwJUfviYQhLQaKo7IUyazMpCrDTB86XN8GYbMudJ51ZYZy0fnwP99nvfx9TuCkQgsaEYrFxKCQuYpLa_4F2rv9667b-P7UXJtue2uO1ran_XjfvUD_ubk-P_WuHR_HZnyAXdfDIuYDTZOeF_mmbL5_ANehVXU.FP8ciw.r527vYu3wKtb0JQY8EBfqjbik5A'
        })
        if respond.status_code == 200:
            if respond.json()['stat'] == 1:
                logging.info('success')
                id_dict = {
                    'call_lead_id': respond.json()['data']['label_detail']['call_lead_id'],
                    'call_detail_id': respond.json()['data']['label_detail']['call_detail_id']
                }
                logging.debug(f'id_dict:\n{id_dict}')
                return id_dict
            elif respond.json()['stat'] == 0:
                msg = respond.json()['msg']
                logging.info('NOT FOUND...reason:%s' % mian_process.decode_msg(msg))
                time.sleep(20)
        else:
            # 有时候会自动退出 标注平台抽风 所以出现这种状态 要再次循环
            logging.error('requested fail')
            mian_process.decode_msg(respond)
            time.sleep(10)
    return respond


if __name__ == "__main__":
    initial_logging()
    mission_info = {
        'name': '验收流程测试01',
        'graph_id': '618b68c394b3a13ac77bc2a4',
        'version_id': '619e4bc694b3a1459e0bffa8',
        'call_line_model': 2,
        'call_port_ids': '61d8f87494b3a10bf1330ae0',
        'robot_ids': '6007e320e2854809335fa095',
        'smart_diagnose_trigger': 1,
        'smart_diagnose_config': '{"open_filter_by_number":true,"harass_rule":{"filter_by_call_result":{"trigger":false},"filter_by_intention_result":{"trigger":false,"options":[]},"filter_by_days_anti_harass":{"trigger":false}}}',
        'showRule': 'false',
        'sms_trigger': 0,
        'is_transfer': 0,
        'smart_schedule_trigger': 1,
        'is_timed_task': 0,
        'redial_trigger': 0,
        'label_type': 1,  # 寸草/地产
        'label_trigger': 1,
        'cc_assign_trigger': 1,
        'cc_assign_strategy': 2,
        'label_intentions': '1s即可,AI推荐',
        'cc_assign_ids': '618b674f97e9717f37a8be8f_564609786' # jiahua 61dc010797e971253dc4577a_779901499 chen 618b674f97e9717f37a8be8f_564609786
    }
    cookie = mian_process.get_cookie()
    task = create_sdk_mission(info=mission_info, cookies=cookie,
                              contacts=[(17520544566, '联系人', '公司'), (18218644344, '联系人', '公司')])
    if type(task) == str:
        # 启动任务
        mian_process.start_mission(task_id=task, cookies=cookie)
        # 检查任务完成情况
        mian_process.is_finish_mission(task_id=task, cookies=cookie)
        # 获取可标注号码
        call_id_list = mian_process.get_call_id_list(task_id=task, cookies=cookie)
        # 第一次标注
        for call_id in call_id_list:
            mian_process.ask_mark_platform(call_id)
    #     # 外呼工作台
    # # 第二次标注
    # check_push_mark_platform()
