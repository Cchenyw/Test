import pandas as pd
from openpyxl import Workbook

filename = "C:\\Users\\TUNGEE\\Desktop\\数据流\\广东盲区号码.xlsx"
s_num = 5
save_path = 'C:\\Users\\TUNGEE\\Desktop\\数据流\\excel_spilt\\'


def spilt_rows(excel_file, spilt_num):
    # 解析excel表
    xlsx = pd.ExcelFile(excel_file)
    data = pd.read_excel(xlsx, sheet_name="sheet1")
    df = pd.DataFrame(data)
    # 获取行数 shape[1]获取列数
    rows = data.shape[0]

    if rows % spilt_num == 0:
        clc_num = int(rows / spilt_num)
    else:
        clc_num = int(rows / spilt_num) + 1
    for index in range(0, clc_num):
        start_i = spilt_num * index
        phone_number_list = []
        for i in range(start_i, start_i + spilt_num):
            phone_info = []
            contacts = df['联系人'][i]
            phone_info.append(contacts)
            company = df['企业名称'][i]
            phone_info.append(company)
            phone_number = df['被叫号码'][i]
            phone_info.append(str(phone_number))
            phone_number_list.append(phone_info)
        # phone_number_list.append('######')
        save_in_excel(number_list=phone_number_list, seq=[start_i, start_i + spilt_num])
    return phone_number_list


def save_in_excel(number_list, seq):
    df = pd.DataFrame(number_list, columns=['联系人', '企业名称', '被叫号码'])
    if len(seq) != 2:
        print('seq:参数异常')
    else:
        global save_path
        df.to_excel(f'{save_path}test_save_to_excel{seq[0]}-{seq[1]}.xlsx', index=False)


if __name__ == "__main__":
    # my_list = spilt_rows(filename, 10000)
    # print(my_list)
    # my_number_list = ['1', '2', '3']
    # save_in_excel(my_number_list)
    my_list = spilt_rows(filename, s_num)
