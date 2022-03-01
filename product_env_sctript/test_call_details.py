import time
from concurrent.futures import ThreadPoolExecutor
import threading

import requests


def get_number_preview():
    # 线程名称
    thread_name = threading.current_thread().name
    url = 'https://call.tungee.com/api/call-details/number-preview'
    header = {
        'referer': 'https://call.tungee.com/call-records',
        # 'content-type': 'multipart/form-data',默认是这种格式的了 无需再传
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 97.0.4692.71Safari / 537.36Edg / 97.0.1072.55',
        'Cookie': 'tg_referrer_source=https%3A%2F%2Fuser.tungee.com%2F;crm_canary_ver=v2.8.7-beta.1;Hm_lvt_b59f3bbf17edc1719f335e2529efaab4=1640759280,1641866801,1642060379; Hm_lpvt_b59f3bbf17edc1719f335e2529efaab4=1642060399;accountCenterSessionId=.eJwtjkFLxDAQhf9Lzx6SzKTN7E1wEcEWRIqslzKZTFzrtsK2ulDxvxvU4-O9j_d9VR-LnofXVO2q2krMWbVW0UgQsImO2YXqqpIjz7OeyuiiseTlFziM-60be2hv-_V5fNm6R2O68Q3un-58u12v3dRie7OHw9T7dnq4FPDvSSEbJyDUJGgACEkdWsNZkuVshRE4BhKXwGSkxhmS4ByYQN4oggO2gNr4FDJICrF0PmbrC81oOVJASUSJI1t0ILVTRCGTslVrfRGZVdOw8KcO6_uQYrXLfFq0COazLsf_-P0DHqVVvw.FMFygA.dfBlN9FGt9CTeYPhRl3p80uI0eg'
    }
    data = {
        'intentions': '[]',
        'begin': 0,
        'query_type': 1,
        'results': '[]',
        'mark_intentions': '',
        'end': 50,
        'transfer_intentions': '[]',
        'durations': '[]'
    }
    res = requests.post(url=url, headers=header, data=data)
    res_json = res.json()
    if res.status_code == 200:
        number_preview_id = res_json.get('number_preview_id')
        print(f'线程：{thread_name},任务id：{number_preview_id},预请求成功\n')
        get_number_preview_status(number_preview_id, count=0)
    else:
        sub_msg = res_json.get('sub_msg')
        print(sub_msg.encode().decode())


def get_number_preview_status(task_id, count):
    # 线程名称
    thread_name = threading.current_thread().name
    url = f'https://call.tungee.com/api/call-details/number-preview?number_preview_id={task_id}'
    header = {
        'referer': 'https://call.tungee.com/call-records',
        'user-agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 97.0.4692.71Safari / 537.36Edg / 97.0.1072.55',
        'Cookie': 'tg_referrer_source=https%3A%2F%2Fuser.tungee.com%2F;crm_canary_ver=v2.8.7-beta.1;Hm_lvt_b59f3bbf17edc1719f335e2529efaab4=1640759280,1641866801,1642060379; Hm_lpvt_b59f3bbf17edc1719f335e2529efaab4=1642060399;accountCenterSessionId=.eJwtjkFLxDAQhf9Lzx6SzKTN7E1wEcEWRIqslzKZTFzrtsK2ulDxvxvU4-O9j_d9VR-LnofXVO2q2krMWbVW0UgQsImO2YXqqpIjz7OeyuiiseTlFziM-60be2hv-_V5fNm6R2O68Q3un-58u12v3dRie7OHw9T7dnq4FPDvSSEbJyDUJGgACEkdWsNZkuVshRE4BhKXwGSkxhmS4ByYQN4oggO2gNr4FDJICrF0PmbrC81oOVJASUSJI1t0ILVTRCGTslVrfRGZVdOw8KcO6_uQYrXLfFq0COazLsf_-P0DHqVVvw.FMFygA.dfBlN9FGt9CTeYPhRl3p80uI0eg'
    }
    res = requests.get(url=url, headers=header)
    res_json = res.json()
    if res.status_code == 200:
        if res_json.get('is_building') == 0:
            print(f'线程：{thread_name},任务id：{task_id},请求正常\n')
        elif res_json.get('is_building') == 1:
            time.sleep(1)
            count += 1
            print(f'线程：{thread_name},任务id：{task_id},第{count}次尝试\n')
            get_number_preview_status(task_id, count=count)
        else:
            print(res_json)
    else:
        print(res_json)


if __name__ == "__main__":
    pool = ThreadPoolExecutor()
    for i in range(3):
        pool.submit(get_number_preview)
