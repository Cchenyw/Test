import random

import pandas as pd


def remix_call_number(file_path):
    excel_file = pd.ExcelFile(open(file_path, 'rb'))
    data = pd.read_excel(excel_file)
    df = pd.DataFrame(data)
    rows = df.shape[0]
    for index in range(0, int(rows / 2)):
        random_i = random.randint(0, rows)
        random_j = random.randint(0, rows)
        if random_i != random_j:
            exchange_number = []
            contacts = df['联系人'][random_i]
            exchange_number.append(contacts)
            company = df['企业名称'][random_i]
            exchange_number.append(company)
            phone_number = df['被叫号码'][random_i]
            exchange_number.append(str(phone_number))



if __name__ == "__main__":
    fp = "C:\\Users\\TUNGEE\\Desktop\\数据流\\随机打乱号码.xlsx"
    remix_call_number(fp)
