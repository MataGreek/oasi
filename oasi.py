from ast import arg, parse
from base64 import decode
from cmath import e
import encodings
from logging import exception
from re import L
from tabnanny import check
from unicodedata import name
import requests as r
import http.client as httplib
import urllib
import socket
import urllib.request
import urllib3
import sys
import time
import colorama
colorama.init()

yes_choice = ['', 'Yes', 'y', 'Y', 'yes', 'YES']
no_choice = ['No', 'n', 'no', 'NO', 'N']


def check_updates():
    try:
        conn = httplib.HTTPSConnection("raw.githubusercontent.com")
        conn.request("GET", "/MataGreek/oasi/main/core/version.txt")
        repver = conn.getresponse().read().strip().decode()
        with open('./core/version.txt') as vf:
            global currentVersion
            currentVersion = vf.read().strip()

        if repver == currentVersion:

            print("")
        else:
            ask = input(b"  [+] Version "+str(repver) +
                        b" Is Available! Do you want to update? [Y/n]:   ")

            if ask in yes_choice:

                print("")

                print(b"  [!] Updating... Please do not close your application.")

                print("")

                time.sleep(4)

                try:

                    conn.request(
                        "GET", "/MataGreek/oasi/main/oasi.py")

                    newCode = conn.getresponse().read().strip().decode()

                    with open('oasi.py', 'w+') as gr:

                        currentgr = gr.read().strip()

                        if newCode != currentgr:

                            gr.write(newCode)

                except KeyboardInterrupt:

                    print(b"Exit.")
                try:

                    conn.request(
                        "GET", "/MataGreek/oasi/main/requirements.txt")

                    newcode11 = conn.getresponse().read().strip().decode()

                    with open('requirements.txt', 'w+') as req:

                        currentreq = req.read().strip()

                        if newcode11 != currentreq:

                            req.write(newcode11)

                except KeyboardInterrupt:

                    print(b"exit.")
                try:

                    conn.request(
                        "GET", "/MataGreek/oasi/main/wordlist/simple_wl.txt")

                    newcode10 = conn.getresponse().read().strip().decode()

                    with open('./wordlist/simple_wl.txt', 'w+') as st:

                        currentst = st.read().strip()

                        if newcode10 != currentst:

                            st.write(newcode10)

                except KeyboardInterrupt:

                    print(b"exit.")
                    print(b"")

                    print(b"  [+] Updated!")

                    time.sleep(1)

                    print(b"")
                    print(
                        b" RESTART THE PROGRAM FOR UPDATES TAKE AFFECT")
                    print(b"")

                    pass

                    if repver != currentVersion:

                        with open('./core/version.txt', 'w+') as pf:

                            pf.write(repver)

                    else:

                        print(b" [!] Your version is:", currentVersion +
                              b"You are not up to date! Please update the program.")

    except KeyboardInterrupt:

        print(b"")

    except Exception as e:

        print(b"Unable to Check for Update, Error:", str(e))


check_updates()


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, metavar='',
                        required=True, help='Insert the target URL')
    # parser.add_argument('-o', '--output', type=str, metavar='',
    #                     required=False, help='Create output file')
    parser.add_argument('-w', '--wordlist', type=str, metavar='',
                        required=False, help='Enter wordlist file (Leave it empty for default wordlist)')
    return parser.parse_args()


def Banner():
    print(f"""
    
   ____           _____ _____ {currentVersion}
  / __ \   /\    / ____|_   _|
 | |  | | /  \  | (___   | |  
 | |  | |/ /\ \  \___ \  | |  
 | |__| / ____ \ ____) |_| |_ 
  \____/_/    \_\_____/|_____|
                              
                              

  |  -----------------------------------------------------------
  |  Author: Mata
  |  Donation: https://www.buymeacoffee.com/mataroot
  |  -----------------------------------------------------------

    """)


def parse_url(url):
    try:
        host = urllib3.util.url.parse_url(url).host
    except Exception as e:
        print("")
        sys.exit(1)
    return host


def check_host():
    time.sleep(1)
    print(f"""
-----------
   Host
-----------
    """)
    print(b"Checking Target...")
    time.sleep(2)
    args = parse_args()
    global target
    target = parse_url(args.url)
    global host
    host = socket.gethostbyname(target)
    print(f"\nTarget IP address: {host}\n")


def check_subdomains():
    time.sleep(1)
    print(f"""
-----------
Subdomains
-----------
    """)

    subdomains = []
    print(b"Checking possible Subdomains...\n")
    req = r.get(f"https://crt.sh/?q=%.{target}&output=json")

    if req.status_code != 200:
        print(b"info not available")
        sys.exit(1)

    for (key, value) in enumerate(req.json()):
        subdomains.append(value['name_value'])
    subs = sorted(set(subdomains))
    for s in subs:
        print(f'{s}')


def dnslookup():
    time.sleep(1)
    print(f"""
-----------
DNS Lookup
-----------
    """)
    count = 1

    urlsweb = []
    try:
        borders = []
        targeturl = f"https://api.programion.com/dns/dnsjson.php?api_key=a63233b816dfd48d392c4a4491d82008&domain={target}"
        for line in urllib.request.urlopen(targeturl):
            newurl = str(line)
            urlsweb.append(newurl)
            print(newurl)
            count += 1
        print(f"\n\nFound: {count} Results!")
    except KeyboardInterrupt:
        print(b"\n Exiting Dns Lookup...")
        pass
        time.sleep(1)


def reverseip():
    time.sleep(1)
    print(f"""
-----------------------------------
Checking Domains On the same Host
-----------------------------------
    """)

    urlsweb = []
    try:
        borders = []
        targeturl = f"https://api.viewdns.info/reverseip/?host={target}&apikey=c9ce6f82bb48fed1383384feba956888cd1c8973&output=json"
        for line in urllib.request.urlopen(targeturl):
            newurl = str(line)
            urlsweb.append(newurl)
            print(newurl)
    except KeyboardInterrupt:
        print(b"\n Exiting Dns Lookup...")
        pass
        time.sleep(1)


def check_ports():
    time.sleep(1)
    print(f"""
-----------
Usual Ports
-----------
    """)

    print(b"\nChecking usual Ports...\n")
    time.sleep(1)
    try:
        for port in range(1, 3306):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.5)

            result = s.connect_ex((host, port))
            if result == 0:
                sn = socket.getservbyport(port)
                print(b"[*] Port {} is open".format(port) +
                      b"    Service: ", sn)

                s.close()
    except KeyboardInterrupt:
        print(b"\n Exiting Port Scanner...")
        pass
        time.sleep(1)

    except socket.error:
        print(b"\n Host is not responding...")
        sys.exit()


def inputer():
    user_choice = input(b"\n\nDo you want to continue the scanning?(Y/n): ")

    if user_choice in yes_choice:
        pass
    if user_choice in no_choice:
        print(b"Exiting...")
        sys.exit()


def check_dirs():
    time.sleep(1)
    print(f"""
-------------------
Directory Scanning
-------------------
""")
    args = parse_args()
    if args.wordlist is None:
        wlist = open('wordlist/default_wl.txt', 'r')
        content = wlist.read()
        wordlist = content.splitlines()
        word = args.wordlist
        for path in wordlist:
            link = f"https://{target}/{path}"
            try:

                req = r.get(link)
                if req.status_code == 200:
                    print(b"\n[+] Directory Found: ", str(link) +
                          b"   (Status: " + str(req.status_code) + ")    ")
                if req.status_code != 200:
                    spaces = ' ' * 10
                    print(b"\rScanning: " + str(path) + str(spaces), end='')

            except KeyboardInterrupt:
                print(b"\n[!] Exit.")
                sys.exit()
                pass
    if args.wordlist is not None:
        wlist2 = open(args.wordlist, 'r')
        content2 = wlist2.read()

        wordlist2 = content2.splitlines()
        word2 = args.wordlist
        for path in wordlist2:
            link2 = f"https://{target}/{path}"
            try:

                req2 = r.get(link2)
                if req2.status_code == 200:
                    print(b"\n[+] Directory Found: ", str(link2) +
                          b"   (Status: " + str(req2.status_code) + ")    ")
                if req2.status_code != 200:
                    spaces = ' ' * 10
                    print(b"\rScanning: " + str(path) + str(spaces), end='')

            except KeyboardInterrupt:
                print(b"\n[!] Exit.")
                sys.exit()


def main():
    Banner()
    time.sleep(1)
    check_host()
    time.sleep(1)
    dnslookup()
    time.sleep(1)
    reverseip()
    time.sleep(1)
    check_subdomains()
    time.sleep(1)
    inputer()
    time.sleep(1)
    check_dirs()
    time.sleep(1)
    check_ports()


if __name__ == '__main__':
    main()
