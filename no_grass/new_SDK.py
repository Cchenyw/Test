import json
import time
import logging

import requests

import no_grass.mian_process

test = 'https://call-test.tangees.com'
base_url = test


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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    mission_info = {
        'name': '冒烟测试07',
        'graph_id': '6184ad0aa3552266652dccf5',
        'version_id': '619e5cb0a355220c66266133',
        'call_line_model': 2,
        'call_port_ids': '61d6a114a35522259f5fe5c7',
        'robot_ids': '6007e320e2854809335fa09b',
        'smart_diagnose_trigger': 1,
        'smart_diagnose_config': '{"open_filter_by_number":true,"harass_rule":{"filter_by_call_result":{"trigger":false},"filter_by_intention_result":{"trigger":false,"options":[]},"filter_by_days_anti_harass":{"trigger":false}}}',
        'showRule': 'false',
        'sms_trigger': 0,
        'is_transfer': 0,
        'smart_schedule_trigger': 1,
        'is_timed_task': 0,
        'redial_trigger': 0,
        'label_type': 2,
        'label_trigger': 1,
        'cc_assign_trigger': 1,
        'cc_assign_strategy': 2,
        'label_intentions': '一秒就行,AI推荐',
        'cc_assign_ids': '6185e2aa283ae57b54afe893_498300240'
    }
    cookie = no_grass.mian_process.get_cookie()
    task = create_sdk_mission(info=mission_info, cookies=cookie,
                              contacts=[(17520544566, '公司', '联系人'), (18218644344, '公司', '联系人')])
    print(task)
    no_grass.mian_process.is_finish_mission(task, cookie)
