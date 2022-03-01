import requests

body = {
    'phone': '17520544566',
    'password': '69b77fe60044a9706bddd58cd37373d6',
    'remember': 0,
    'code': None,
    'area_code': 86
}
# respond = requests.post('http://user-dev.tangees.com/api/individual-user/login', data=body)
# cookies = requests.utils.dict_from_cookiejar(respond.cookies)
# print(respond.text)
# print(cookies)
# cookie = ''
# for name, value in cookies.items():
#     cookie = f'{name}={value}'
#     print(cookie)
header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'Connection': 'keep-alive',
    'pragma': 'no-cache',
    'Referer': 'http://company-dev.tangees.com/call-center/tasks/preparing',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
#
# respond2 = requests.get('http://call-dev.tangees.com/api/tasks/draft?begin=0&end=10', headers=header)
# print(respond2.text)
# session = requests.session()
# respond3 = session.post('http://user-dev.tangees.com/api/individual-user/login', data=body)
# print(respond3.text)
# print(respond3.cookies)
# header1 = {
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'cache-control': 'no-cache',
#     'Connection': 'keep-alive',
#     'pragma': 'no-cache',
#     'Host': 'user-dev.tangees.com',
#     'Referer': 'http://user-dev.tangees.com/',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
# }
# respond5 = session.get('http://user-dev.tangees.com/api/individual-user/profile', headers=header1)
# print(respond5.status_code)
# print(respond5.cookies)
# header2 = {
#     'Accept': '*/*',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'cache-control': 'no-cache',
#     'Connection': 'keep-alive',
#     'pragma': 'no-cache',
#     'Host': 'call-dev.tangees.com',
#     'Referer': 'http://call-dev.tangees.com/call-center/tasks/preparing',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
# }
# respond6 = session.get('http://call-dev.tangees.com/api/tasks/draft?begin=0&end=10', headers=header2)
# print(respond6.text)
# print(respond6.cookies)
# print(session.cookies)
header = {
    'Cookie': 'accountCenterSessionId=.eJwlzr1uhDAQBOB3cX2F117_UZ5OShNyDSiCBtnete4QIhJwiUiUdw9JuinmG82XGO4kKgExcQxeFqfQoCxgQiGFiOCVogIeXQLU0iOjVdnEnNmn4FGTYsrBeRu8NiC9lqSxGNaGmEgm67O2CclAIS6SwGUwSSqSnDxkxTFRyuIkZmYa1vjOw_Y2UBJVidPKJ_FYefk_aUFnZBeKczZbwwymwBEOPJSF15uotuVxkPWvfm1q86LavR_z1l_OY71L2Y0dPjfTWH_WW_fa6r7p9uvlfK-f2t-ZfIvzzNOBPziJ7x_jsFVG.FB3gcQ.CvgYglKkgk-R_KQlQX1-eWLe0xY'
}
respond = requests.get('http://call-dev.tangees.com/api/tasks/draft?begin=0&end=10', headers=header)
print(respond.text)
