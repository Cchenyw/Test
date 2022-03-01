from collections import Counter

import pandas as pd
import re


def result_for_call(file_path):
    # 靓号
    good_number_count = 0
    # 总接通电话数
    total_received_number_count = 0
    # 过滤掉靓号
    # 接通数
    received_number_count = 0
    # 固话过滤数量
    fixed_number_count = 0
    # 线路盲区数量
    blind_number_count = 0
    # 空号数量
    null_number_count = 0
    # 被叫停机数量
    suspended_number_count = 0
    # 黑名单数量
    black_number_count = 0
    data = pd.read_json(open(file_path, 'r'), lines=True)
    print(data)
    for index in range(0, data.shape[0]):
        if data['result'][index] == 1:
            total_received_number_count += 1
        if check_low_wish(str(data['number'][index])):
            good_number_count += 1
        else:
            if data['result'][index] == 1:
                received_number_count += 1
            elif data['result'][index] == 16:
                fixed_number_count += 1
            elif data['result'][index] == 13:
                blind_number_count += 1
            elif data['result'][index] == 4:
                null_number_count += 1
            elif data['result'][index] == 14:
                black_number_count += 1
            elif data['result'][index] == 10:
                suspended_number_count += 1

    print(f'当日呼叫总数:{data.shape[0]}')
    print('由于按顺序进行规则触发，靓号数量（意愿低）中，先于线路盲区和固话过滤,部分固话和盲区会归为意愿低')
    print(f'总接通电话数为:{total_received_number_count}')
    print(f'靓号数(意愿低)为:{good_number_count}')
    print(f'固话过滤数为:{fixed_number_count}')
    print(f'盲区数量为:{blind_number_count}')
    print(f'空号数量为:{null_number_count}')
    print(f'黑名单数量为:{blind_number_count}')
    print(f'停机数量为:{suspended_number_count}')
    print(f'线上初始接通率:{total_received_number_count / data.shape[0]}')
    print(
        f'产品上线后，保守预估接通率提升至:{received_number_count / (data.shape[0] - good_number_count - fixed_number_count - blind_number_count)}')
    print(
        f'接通率期待值:{received_number_count / (data.shape[0] - good_number_count - fixed_number_count - blind_number_count - null_number_count - black_number_count - suspended_number_count)}')


def check_low_wish(number):
    """通话意愿低"""
    reg = re.compile('01234567890')
    reg_str = number[-4:]
    if reg.search(reg_str):
        return True
    if len(Counter(reg_str)) <= 2:
        return True
    return False


if __name__ == "__main__":
    result_for_call('C:\\Users\\TUNGEE\\Desktop\\项目\\智能呼叫v4.0.0\\call.txt')
