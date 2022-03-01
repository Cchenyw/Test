import requests
import pandas as pd
import re

from contextlib import closing


def get_url(url, headers, save_path):
    response = requests.get(url=url, headers=headers)
    json_data = response.json()
    qa_list = json_data['categories'][0]['qa_list'][0:]
    questions = pd.DataFrame(qa_list, columns=['a_voice_download_url', 'a_text'])
    for index in range(questions.shape[0]):
        r = '[，。！？、]'
        file_name = re.sub(r, '', str(questions['a_text'][index]))
        download_file(questions['a_voice_download_url'][index], f"{save_path}{file_name}.wav")


def download_file(url, path):
    voice_file = requests.get(url)
    with open(path, 'wb') as f:
        f.write(voice_file.content)
    f.close()
    print(path)


if __name__ == "__main__":
    re_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "cookie": "monitorCustomerKey=88c01f88-ebb7-4861-a2e8-e0011e7c0b30-20210712094415; _ga=GA1.2.2123651635.1627455950; Qs_lvt_309705=1627455950%2C1627522565%2C1628562073%2C1629814238%2C1629877074; Qs_pv_309705=1126022115317719400%2C3138813395397076000%2C3215665019010110500%2C150751322647353600%2C2534261441987935700; Hm_lvt_d3ee3af8af62f47558a292277356e90f=1627522565,1628562074,1629814239,1629877075; Hm_lpvt_d3ee3af8af62f47558a292277356e90f=1629877075; webfunny_ip=61.144.144.236; webfunny_province=%E5%B9%BF%E4%B8%9C%E7%9C%81%E5%B9%BF%E5%B7%9E%E5%B8%82%E5%A4%A9%E6%B2%B3%E5%8C%BA; Hm_lvt_b59f3bbf17edc1719f335e2529efaab4=1629943550,1629965611,1630032940,1630052151; tg_referrer_source=direct; Hm_lpvt_b59f3bbf17edc1719f335e2529efaab4=1630052166; accountCenterSessionId=.eJwlzslOwzAUheF38boLD_G1nR2iXVQirZCySTeR7-AOCkFKUkBFvDsRPMB3zv-t-jLJfFH1Mt1lo-6zTP2VVa3A2JiKjSAkmKqqQog-EKmNGkW4n_OH9Mt7z6jqkod5xfMf7G6dPthXfWz3S3fbmeZZ61N7ur60Z9O13XLc7r4OjyfbbM--eQxv6-D_o0hkstp771yBAE4Hn7EwF8KcqSInkJm0dyGaVEVnkJhNIaMJhFPWQXBlHDgmD4AcdMKArqKE0ZocgXMGG4O3UQpjhiTJGEgBsUhcQ-iSx1GGNeZTUP38AinNVdU.FAoxtg.OfF3qGY9DmJo8yHlP0dJn1c7WmQ; smartVoiceSessionId=eyJfZnJlc2giOmZhbHNlLCJ1c2VyX2lkIjoiNjBlMjg1ZDM2ZWNlYjkxYzZkOWJhYjc3In0.FAox1g.hGAvz_IKbu654fUP0H20e0WZl04",
        "pragma": "no-cache",
        "referer": "https://call.tungee.com/graphs/graph-intention-invitation/5f27db886938c67db050f97c/knowledge-base?isDisabled=true&versionId=5f27db886938c67db050f97d",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73"
    }
    re_url = "https://call.tungee.com/api/graph/5f27db886938c67db050f97c/kb?version_id=5f27db886938c67db050f97d"
    sp = "C:\\Users\\TUNGEE\\Desktop\\数据流\\录音文件\\"
    get_url(url=re_url, headers=re_headers, save_path=sp)
