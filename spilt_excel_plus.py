import pandas as pd

import argparse


# 获取行数
def get_row(data):
    if data == 0:
        row = 0
        print('获取行数失败')
    else:
        row = data.shape[0]
    return row


# 获取columns
def get_columns(data):
    if data == 0:
        columns = 0
        print('获取键值失败')
    else:
        columns = data.columns
    return columns


# 解析excel文档
def get_data_from_excel(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        # 默认取第一张表
        data = pd.read_excel(xls, 0)

    except Exception as e:
        data = 0
        print('获取文件失败:', e)
    return data


# excel文档分块 --返回分块数
def get_block_num(rows, spilt_num):
    # 切分的份数
    if rows / spilt_num > 1:
        if rows % spilt_num == 0:
            return rows % spilt_num
        else:
            return int(rows / spilt_num) + 1
    else:
        print(f'excel文件行数不能小于分割行数（文件行数:{rows},分割行数：{spilt_num}）!')
        return 0


# 判断剩余行数是否大于可分割行数 --取最小行数
def get_mini_rows(rows, start_i, spilt_num):
    # 剩余行数
    remain_rows = rows - start_i
    # 取最小行数
    if remain_rows >= spilt_num:
        return start_i + spilt_num
    else:
        return start_i + remain_rows


# 处理块元素
def handle_row_data(data, start_i, end_i):
    df = pd.DataFrame(data)
    # 直接这样读不需要知道列数，一次保存一行中多个列
    lines = df[0:][start_i:end_i]
    seq = [start_i, end_i]
    return lines, seq


# 保存到excel
def save_to_excel(lines, save_path, seq):
    df = pd.DataFrame(data=lines, columns=get_columns(lines))
    try:
        df.to_excel(f'{save_path}excel_spilt_file_{seq[0]}-{seq[1]}.xlsx', index=False)
        print(f"文件:'excel_file_spilt:{seq[0]}-{seq[1]}',保存成功!")
    except FileExistsError as fn:
        print('获取文件路径失败!')
        exit(1)


def func_spilt_excel_file(origin_path, save_path, spilt_num):
    # 解析excel
    data = get_data_from_excel(origin_path)
    if data == 0:
        exit(1)
    # 获取行数
    rows = get_row(data)
    if rows == 0:
        exit(1)
    # 获取分割块数
    block_num = get_block_num(rows, spilt_num)
    # 切分文件，保存excel
    for index in range(0, block_num):
        start_i = rows * index
        end_i = get_mini_rows(rows, start_i, spilt_num)
        lines, seq = handle_row_data(data, start_i, end_i)
        print(f'===剩余行数：{rows - start_i}，切分行数：{num}，第{index + 1}份文件,切分序列：{seq[0]}-{seq[1]}===')
        save_to_excel(lines, save_path, seq)


# 集成到命令行执行
def handle_cmd():
    parser = argparse.ArgumentParser(prog='spilt excel file',
                                     description='This script was used to spilt the excel file to smaller excel file')
    parser.add_argument('-n', metavar='split_num', type=int, required=True, help='切分行数：split_num')
    parser.add_argument('-f', metavar='origin_file_path', type=str, required=True, help='源文件地址：origin_file_path')
    parser.add_argument('-s', metavar='save_path', type=str, required=True, help='保存文件地址：save_path')
    args = parser.parse_args()
    print(args)
    # 调用函数处理
    spilt_num = args.n
    origin_file = args.f
    save_path = args.s
    func_spilt_excel_file(origin_file, save_path, spilt_num)


# 测试
if __name__ == "__main__":
    my_excel_file = 'C:\\Users\\TUNGEE\\Desktop\\数据流\\1-1000.xlsx'
    sp = 'C:\\Users\\TUNGEE\\Desktop\\数据流\\excel_spilt\\'
    num = 1000
    func_spilt_excel_file(my_excel_file, sp, num)
    # handle_cmd()
