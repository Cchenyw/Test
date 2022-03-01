import requests


def upload_file(file_path, address, header):
    with open(file_path, 'rb') as f:
        respond = requests.post(address, headers=header, data=f)
    print(respond.text)


if __name__ == "__main__":
    excel_file = 'C:\\Users\\TUNGEE\\Desktop\\数据流\\格式错误全部被过滤号码包.xlsx'
    http_address = 'http://call-dev4.tangees.com/api/task/61139c2aed871319f83aded4/numbers/upload'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'sessionId=.eJw1zk2KAkEMQOG71HoWqVTSSXkZqfwxLpSh1ZV4dxtk4K0f36uda8_7bzs99mf-tPMl2qmpVJmQE0YmIlcUoq8-MZxBB3Fy0tBlpYI2rQCEY3WjKZ2hC5suCB8Z1v1okgDyliDl2zAw24jjuPBaNUt7ekxXzaQ1oB2Qv9yv65a3xz_tec_9y9ugKNKIQGYgOKT6HBbt_QHH-j1E.E_YllQ.aCUKFGx1vZQ1PWfC1U0pk-JOxfQ; accountCenterSessionId=.eJwljUFLxDAQhf9LznuYpJkm6U3Yy4pbWVGkvZSZZEJbaoW2q7jif7covNt73_u-VexpnmVSlfoUVgfV5UXWXlXbcpWDuq6ydEPa21JrGyBEcJopapO885SRdmT9G9TjNDwe78fm9rI1tzusB4BmvJiH15M-vzVbPT6N7fPpqz1ezPnY9js4i6RupQ_ptvcusaoyTetu_Td6lzM7G61JIsZgTtmYSDqYFBF8YVFQbOGJs3eGA2cAh4k02-A0gnbIniDFQhLruCdYBwZLAZdjWTAwlxbT_oJEOWSvJaYQvRexVID6-QV7D1ZY.E_Yr7g.WfirtYRuzXuhEzBEdwA51PODJTc',
        'Host': 'call-dev4.tangees.com',
        'pragma': 'no-cache',
        'Referer': 'http://call-dev4.tangees.com/call-center/tasks/detail?id=61138f05ed871344462716d5',
        'User - Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML, likeGecko)Chrome/91.0.4472.164Safari/537.36'
    }
    upload_file(excel_file, http_address, headers)
