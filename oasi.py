from argparse import ArgumentParser
from ast import arg, parse
from base64 import decode
from cmath import e
import encodings
from logging import exception
from re import L
import re
from tabnanny import check
from unicodedata import name
from weakref import proxy
import requests as r
import http.client as httplib
import urllib
import socket
import urllib.request
import urllib3
import sys
import time
from tqdm import tqdm, tgrange
import colorama
from colorama import *
colorama.init()

yes_choice = ['', 'Yes', 'y', 'Y', 'yes', 'YES']
no_choice = ['No', 'n', 'no', 'NO', 'N']


# def check_updates():
#     try:
#         conn = httplib.HTTPSConnection("raw.githubusercontent.com")
#         conn.request("GET", "/MataGreek/oasi/main/core/version.txt")
#         repver = conn.getresponse().read().strip().decode()
#         with open('./core/version.txt') as vf:
#             global currentVersion
#             currentVersion = vf.read().strip()

#         if repver == currentVersion:

#             print("")
#         else:
#             ask = input("  [+] Version "+str(repver) +
#                         " Is Available! Do you want to update? [Y/n]:   ")

#             if ask in yes_choice:

#                 print("")

#                 print("  [!] Updating... Please do not close your application.")

#                 print("")

#                 time.sleep(4)

#                 try:

#                     conn.request(
#                         "GET", "/MataGreek/oasi/main/oasi.py")

#                     newCode = conn.getresponse().read().strip().decode()

#                     with open('oasi.py', 'w+') as gr:

#                         currentgr = gr.read().strip()

#                         if newCode != currentgr:

#                             gr.write(newCode)

#                 except KeyboardInterrupt:

#                     print("Exit.")
#                 try:

#                     conn.request(
#                         "GET", "/MataGreek/oasi/main/requirements.txt")

#                     newcode11 = conn.getresponse().read().strip().decode()

#                     with open('requirements.txt', 'w+') as req:

#                         currentreq = req.read().strip()

#                         if newcode11 != currentreq:

#                             req.write(newcode11)

#                 except KeyboardInterrupt:

#                     print("exit.")
#                 try:

#                     conn.request(
#                         "GET", "/MataGreek/oasi/main/wordlist/simple_wl.txt")

#                     newcode10 = conn.getresponse().read().strip().decode()

#                     with open('./wordlist/simple_wl.txt', 'w+') as st:

#                         currentst = st.read().strip()

#                         if newcode10 != currentst:

#                             st.write(newcode10)

#                 except KeyboardInterrupt:

#                     print("exit.")
#                     print("")

#                     print("  [+] Updated!")

#                     time.sleep(1)

#                     print("")
#                     print(
#                         " RESTART THE PROGRAM FOR UPDATES TAKE AFFECT")
#                     print("")

#                     pass

#                     if repver != currentVersion:

#                         with open('./core/version.txt', 'w+') as pf:

#                             pf.write(repver)

#                     else:

#                         print(" [!] Your version is:", currentVersion +
#                               "You are not up to date! Please update the program.")

#     except KeyboardInterrupt:

#         print("")

#     except Exception as e:

#         print("Unable to Check for Update, Error:", str(e))


# check_updates()


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, metavar='',
                        required=True, help='Insert the target URL')
    # parser.add_argument('-o', '--output', type=str, metavar='',
    #                     required=False, help='Create output file')
    parser.add_argument('-w', '--wordlist', type=str, metavar='',
                        required=False, help='Enter wordlist file (Leave it empty for default wordlist)')
    parser.add_argument('-b', '--batch', type=str, metavar='',
                        required=False, nargs='?', const='', help='Pass all inputs with default (Y/N)')
    parser.add_argument('-s', '--shell', type=str, metavar='', required=False, nargs='?',
                        const='', help='Scan for possible web shells already uploaded in your target')
    return parser.parse_args()


def Banner():
    print(f"""

   ____           _____ _____
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
    print("Checking Target...")
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
    print("Checking possible Subdomains...\n")
    req = r.get(f"https://crt.sh/?q=%.{target}&output=json")

    if req.status_code != 200:
        print("info not available")
        sys.exit(1)

    for (key, value) in enumerate(req.json()):
        subdomains.append(value['name_value'])
    subs = sorted(set(subdomains))
    for s in subs:
        print(f'{s}')


def check_cms():
    print("")
    print("")
    print("""
----------------
CMS Checking...
----------------
        """)

    print("")
    print("")
    time.sleep(2)
    args = parse_args()
    target = parse_url(args.url)
    wpcms = f"http://{target}/wp-content/"
    joomlacms = f"http://{target}/administrator/"
    drupalcms = f"http://{target}/user/login"
    drupalcms2 = f"http://{target}/user/register"
    opencartcms = f"http://{target}/index.php?route=account/register"
    opencartcmslog = f"http://{target}/index.php?route=account/login"
    PrestaShopen = f"http://{target}/en/login?back=my-account"
    PrestaShop = f"http://{target}/login?back=my-account"
    reqwp = r.get(wpcms)
    reqjoomla = r.get(joomlacms)
    reqdrup = r.get(drupalcms)
    reqdrup2 = r.get(drupalcms2)
    reqopencart = r.get(opencartcms)
    reqopencartlog = r.get(opencartcmslog)
    reqprestashopen = r.get(PrestaShopen)
    reqprestashop = r.get(PrestaShop)

    if reqwp.status_code == 200:
        print(Fore.GREEN + "[INFO]" + Fore.RESET +
              " Seems to be a Wordpress CMS")
        print("Tested: " + str(wpcms) + "     " +
              ("(Status: " + str(reqwp.status_code)+")"))
    elif reqjoomla.status_code == 200:
        print(Fore.GREEN + "[INFO]" + Fore.RESET +
              " Seems to be a Joomla! CMS")
        print("Tested: " + str(joomlacms) + "     " +
              ("(Status: " + str(reqjoomla.status_code)+")"))
    elif reqdrup.status_code == 200:
        print(Fore.GREEN + "[INFO]" + Fore.RESET +
              " Seems to be a Drupal CMS")
        print("Tested: " + str(drupalcms) + "     " +
              ("(Status: " + str(reqdrup.status_code)+")"))
    elif reqdrup2.status_code == 200:
        print(Fore.GREEN + "[INFO]" + Fore.RESET + " Seems to be a Drupal CMS")
        print("Tested: " + str(drupalcms2)+" " +
              ("(Status: " + str(reqdrup2.status_code)+")"))
    elif reqopencart.status_code == 200:
        print(Fore.GREEN + "[INFO]" + Fore.RESET +
              " Seems to be a OpenCart CMS")
        print("Tested: " + str(opencartcms)+" " +
              ("(Status: " + str(reqopencart.status_code)+")"))
    elif reqopencartlog.status_code == 200:
        print(Fore.GREEN + "[INFO]" + Fore.RESET +
              " Seems to be a OpenCart CMS")
        print("Tested: " + str(opencartcmslog) + "     " +
              ("(Status: " + str(reqopencartlog.status_code)+")"))
    elif reqprestashopen.status_code == 200:
        print(Fore.GREEN + "[INFO]" + Fore.RESET +
              " Seems to be a PrestaShop CMS")
        print("Tested: " + str(PrestaShopen) + "     " +
              ("(Status: " + str(reqprestashopen.status_code)+")"))
    elif reqprestashop.status_code == 200:
        print(Fore.GREEN + "[INFO]" + Fore.RESET +
              " Seems to be a PrestaShop CMS")
        print("Tested: " + str(PrestaShop) + "     " +
              ("(Status: " + str(reqprestashop.status_code)+")"))
    else:
        print("Can't identify CMS")
        print("")
        print("")
        time.sleep(2)


def upload_directory():
    print("")
    print("")
    print("""
-----------------------------------
Checking for upload directories...
-----------------------------------
    """)
    print("")
    print("")
    time.sleep(2)
    upload_dir_wp = f"http://{target}/wp-content/uploads/"
    upload_dir_simple = f"http://{target}/uploads/"
    request = r.get(upload_dir_simple)
    requestwp = r.get(upload_dir_wp)

    if requestwp.status_code == 200:
        print(Fore.RED + "[IMPORTANT]" + Fore.RESET +
              " Wordpress Upload directory is open: " + upload_dir_wp)
    elif request.status_code == 200:
        print(Fore.RED + "[IMPORTANT]" + Fore.RESET +
              " Upload directory is open: " + upload_dir_simple)
    else:
        print("No Possible upload directory found.")
    time.sleep(2)
    print("")
    print("")


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
        print("\n Exiting Dns Lookup...")
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
        print("\n Exiting Dns Lookup...")
        pass
        time.sleep(1)


def check_ports():
    time.sleep(1)
    print(f"""
-----------
Usual Ports
-----------
    """)

    print("\nChecking usual Ports...\n")
    time.sleep(1)
    try:
        for port in range(1, 3306):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(0.5)

            result = s.connect_ex((host, port))
            if result == 0:
                sn = socket.getservbyport(port)
                print("[*] Port {} is open".format(port) +
                      "    Service: ", sn)

                s.close()
    except KeyboardInterrupt:
        print("\n Exiting Port Scanner...")
        pass
        time.sleep(1)

    except socket.error:
        print("\n Host is not responding...")
        sys.exit()


def inputer():

    args = parse_args()
    if args.batch is None:
        user_choice = input("\n\nDo you want to continue the scanning?(Y/n): ")
        if user_choice in yes_choice:
            pass
        if user_choice in no_choice:
            print("Exiting...")
            sys.exit()
    if args.batch is not None:
        yes_choice


def shell_check():
    print("")
    print("")
    print("""
-----------------------------------
Checking for uploaded Web Shells...
-----------------------------------
    """)
    print("")
    print("")
    args = parse_args()
    if args.shell is None:
        pass
    if args.shell is not None:
        wlist = open('wordlist/shells.txt', 'r')
        content = wlist.read()
        wordlist = content.splitlines()

        print(f"Trying to find uploaded web shells on " +
              Fore.GREEN + str(target) + Fore.RESET + "...")
        print("")
        for path in tqdm(wordlist):
            lnk = f"http://{target}/{path}"
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                    "Accept-Encoding": "*",
                    "Connection": "keep-alive"
                }
                req = r.get(
                    lnk, headers=headers)

                if req.status_code == 200:
                    print(
                        Fore.RED + "\n[!] Possible Web Shell FOUND! : " + str(lnk) + Fore.RESET)

            except Exception as e:
                pass


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
                    print("\n[+] Directory Found: ", str(link) +
                          "   (Status: " + str(req.status_code) + ")    ")
                if req.status_code != 200:
                    spaces = ' ' * 10
                    print("\rScanning: " + str(path) + str(spaces), end='')

            except KeyboardInterrupt:
                print("\n[!] Exit.")
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
                    print("\n[+] Directory Found: ", str(link2) +
                          "   ((Status: " + str(req2.status_code) + ")    ")
                if req2.status_code != 200:
                    spaces = ' ' * 10
                    print("\rScanning: " + str(path) + str(spaces), end='')

            except KeyboardInterrupt:
                print("\n[!] Exit.")
                sys.exit()


def main():
    Banner()
    time.sleep(1)
    check_cms()
    time.sleep(1)
    check_host()
    time.sleep(1)
    dnslookup()
    time.sleep(1)
    reverseip()
    time.sleep(1)
    upload_directory()
    time.sleep(1)
    check_subdomains()
    time.sleep(1)
    inputer()
    time.sleep(1)
    shell_check()
    time.sleep(1)
    check_dirs()
    time.sleep(1)
    check_ports()


if __name__ == '__main__':
    main()
