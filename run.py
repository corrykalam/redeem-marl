import requests, time, sys
from pprint import pprint
req = requests.Session()

def getStr(string,start,end):
	str = string.split(start)
	str = str[1].split(end)
	return str[0]


def getCookies():
    # 0 = cookies
    # 1 = csrf
    # 2 = device_id
    response = req.get('https://www.marlboro.id/auth/login')
    return [response.cookies.get_dict(), getStr(response.text, '<input type="hidden" name="decide_csrf" value="','" />'), response.cookies.get_dict()["deviceId"]]

def getCsrfLogin(cookies):
    response = req.get('https://www.marlboro.id/auth/login', cookies=cookies)
    return getStr(response.text, '<input type="hidden" name="decide_csrf" value="','" />')

def login(email, password, csrf, cookies):
    headers = {
        'sec-fetch-mode': 'cors',
        'origin': 'https://www.marlboro.id',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'referer': 'https://www.marlboro.id/auth/login',
        'authority': 'www.marlboro.id',
        'sec-fetch-site': 'same-origin',
    }
    data = {
    'email': email,
    'password': password,
    'ref_uri': '/',
    'decide_csrf': csrf,
    'param': '',
    'exception_redirect': 'false'
    }
    response = req.post('https://www.marlboro.id/auth/login', headers=headers, data=data, cookies=cookies)
    if "success" in response.text:
        print("Success login to account!")
        return response.cookies.get_dict()
    elif "Email atau password yang lo masukan salah.":
        print("Email atau password yang lo masukan salah")
        return False
    else:
        print("Failed login to account!")
        print(response.text)
        return False
def redeem(devid, session, csrf):
    headers = {
        'origin': 'https://www.marlboro.id',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'accept': '*/*',
        'referer': 'https://www.marlboro.id/discovered/passion-quiz/question-3',
        'authority': 'www.marlboro.id',
        'sec-fetch-site': 'same-origin',
    }
    data = {
    'answer': '2',
    'decide_csrf': csrf,
    }

    cookies = {
        "deviceId": devid,
        "token": "rAYvNP0MGas4CyNDkqMyMd8qE33osGZS",
        "decide_session": session
    }
    response = req.post('https://www.marlboro.id/discovered/passion-quiz-insert', headers=headers, data=data, cookies=cookies)
    if "success" in response.text:
        print("Success redeem point!")
    else:
        print("Failed reedem point!")

file_lurr = input('input nama file: ')
try:
    namefile = open(file_lurr,"r").read().split("\n")
except:
    print("File kg ada lurr!")
    sys.exit(0)
for a in namefile:
    akun_nya = a.split("|")
    email = akun_nya[0]
    password = akun_nya[1]
    print("Eksekusi akun %s"%(email))
    x = getCookies()
    a = login(email, password, x[1], x[0])
    if a != False:
        c = getCsrfLogin(a)
        redeem(x[2], a["decide_session"], c)
    else:
        print("Failed login!")
    req.cookies.clear()
