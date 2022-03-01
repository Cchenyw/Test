import requests
import pandas as pd


def get_response(headers, url):
    response = requests.get(url=url, headers=headers, verify=False)
    json_data = response.json()
    qa_list = json_data['categories'][0]['qa_list'][0:]
    # questions = pd.DataFrame(qa_list, columns=['a_text', 'q_list'])
    # print(questions)
    n_data = pd.json_normalize(qa_list, "q_list",  ["a_list"], errors='ignore')
    print(n_data)
    n_data = n_data.rename(columns={0: 'content', 'a_list': 'expect_reply'})
    print(n_data)
    df = pd.DataFrame(n_data)
    print(df)
    df.to_excel(f"C:\\Users\\TUNGEE\\Desktop\\数据流\\questions\\questions_{n_data.shape[0]}.xlsx", index=False)


if __name__ == "__main__":
    re_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "Connection": "keep - alive",
        "cookie": "accountCenterSessionId=.eJwtjstqwzAQRf9F6y5Gj9Eju4BTKFRe9UG6MRppRGzcFGK3oS7994rQ3b1wD_f8iHxK5zPPYieuTOJOLGNpOW5Rx26e3rr9enx_meII0HdH9fh6gP7peY3T_dhvD9d-23_H7qAa-LnwZbjBVirPDiBYMIXQsVQECXQbDfXCy0nsapoXbvW2z1or8E6hRAukQy0mecKSwRq0QTqViUF77Q0Q6wwEvhIBqvZTq0QowaWaDIMPKAs7DEGmjGyahXYhS6aS0CmW1SVGY20FakgwBWpuXmfmMizpi4f1Yyj0L_j7B3prVFs.FAp4iw.C9VUdYVxy97PsUPRA7QDIbeaNuc",
        "Host": "call-uat.tangees.com",
        "pragma": "no-cache",
        "referer": "https://call-uat.tangees.com/graphs",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73"
    }
    re_url = "https://call-uat.tangees.com/api/graph/6128a8cde28548077f516c51/kb?version_id=6128a8cde28548077f516c52"
    get_response(re_headers, re_url)
    # print(f"总数：{count}")
