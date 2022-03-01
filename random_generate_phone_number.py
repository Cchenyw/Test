import pandas as pd

import random

save_path = 'C:\\Users\\TUNGEE\\Desktop\\数据流\\random_phone_number\\'
company_name = ''
contacts = ''
quantity = '100'


def generate_phone_number(num):
    first_number_list = ['139', '138', '137', '136', '135', '134', '159', '158', '157', '150', '151', '152', '188',
                         '187', '182', '183', '184', '178', '130', '131', '132', '156', '155', '186', '185', '176',
                         '133', '153', '189', '180', '181', '177']
    number_str = '0123456789'
    number_list = []
    for i in range(num):
        global contacts, company_name
        number_info = []
        phone_number = random.choice(first_number_list) + ''.join(random.choice(number_str) for i in range(8))
        # print(phone_number)
        number_info.append(contacts)
        number_info.append(company_name)
        number_info.append(phone_number)
        number_list.append(number_info)
    save_to_excel(number_list)


def save_to_excel(data):
    df = pd.DataFrame(data, columns=['联系人', '企业名称', '被叫号码'])
    global save_path
    df.to_excel(f'{save_path}随机生成号码包{len(data)}.xlsx', index=False)


if __name__ == "__main__":
    generate_phone_number(int(quantity))
