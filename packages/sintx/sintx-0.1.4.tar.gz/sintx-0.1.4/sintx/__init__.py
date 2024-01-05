  return name


import os, json, time
from os import system as sintx
from time import sleep as cd

try:
    import requests
except ModuleNotFoundError:
    sintx("pip install requests")
    import requests

from requests import get as reqg
from requests import post as reqp
from requests import session as reqs

try:
    import ua_generator
except ModuleNotFoundError:
    sintx("pip3 install -U ua-generator")
    import ua_generator

###---------------### COLORS ###--------------- ###

sintx_blue = "\033[94m"
sintx_white = "\033[1;97m"
sintx_cyan = "\033[0;36m"
sintx_yellow = "\033[1;33m"
sintx_black = "\033[0;30m"
sintx_green = "\033[0;32m"
sintx_light_red = "\033[1;31m"
sintx_light_green = "\033[0;37m"
sintx_dark_gray = "\033[1;30m"
sintx_light_purple = "\033[1;35m"
sintx_bold_green = "\033[1;32m"
mxclrs = "38;5"
sintx_red_orange = f"\033[{mxclrs};208m"
sintx_red_blue = f"\033[{mxclrs};32m"
sintx_red_cyan = f"\033[{mxclrs};122m"
sintx_red_green = f"\033[{mxclrs};112m"
sintx_red_purple = f"\033[{mxclrs};147m"

###---------------### YEAR CHECKER ###--------------- ###


def scrape_year(uid):
    D = "20??"
    E = "2023"
    C = "2009"
    B = uid
    if len(B) == 15:
        if str(B)[:10] in ["1000000000"]:
            get_year = C
        elif str(B)[:9] in ["100000000"]:
            get_year = C
        elif str(B)[:8] in ["10000000"]:
            get_year = C
        elif str(B)[:7] in [
            "1000000",
            "1000001",
            "1000002",
            "1000003",
            "1000004",
            "1000005",
        ]:
            get_year = C
        elif str(B)[:7] in ["1000006", "1000007", "1000008", "1000009"]:
            get_year = "2010"
        elif str(B)[:6] in ["100001"]:
            get_year = "2010-2011"
        elif str(B)[:6] in ["100002", "100003"]:
            get_year = "2011-2012"
        elif str(B)[:6] in ["100004"]:
            get_year = "2012-2013"
        elif str(B)[:6] in ["100005", "100006"]:
            get_year = "2013-2014"
        elif str(B)[:6] in ["100007", "100008"]:
            get_year = "2014-2015"
        elif str(B)[:6] in ["100009"]:
            get_year = "2015"
        elif str(B)[:5] in ["10001"]:
            get_year = "2015-2016"
        elif str(B)[:5] in ["10002"]:
            get_year = "2016-2017"
        elif str(B)[:5] in ["10003"]:
            get_year = "2018-2019"
        elif str(B)[:5] in ["10004"]:
            get_year = "2019-2020"
        elif str(B)[:5] in ["10005"]:
            get_year = "2020"
        elif str(B)[:5] in ["10006", "10007"]:
            get_year = "2021"
        elif str(B)[:5] in ["10008"]:
            get_year = "2022"
        elif str(B)[:5] in ["10009"]:
            get_year = E
        else:
            get_year = D
    elif len(B) == 14:
        get_year = E
    elif len(B) in [9, 10]:
        get_year = " 2008-2009 "
    elif len(B) == 8:
        get_year = " 2007-2008 "
    elif len(B) == 7:
        get_year = " 2006-2007 "
    else:
        get_year = D
    return get_year


###---------------### GET FOLLOWERS ###--------------- ###


def scrape_followers(token):
  try:
    followers = reqg(
        f"https://graph.facebook.com/me/subscribers?limit=1000&access_token={token}"
    ).json()["summary"]["total_count"]
    return followers
  except:
    return None

###---------------### GET FRIENDS ###--------------- ###


def scrape_friends(token):
  try:
    friends = reqg(
        f"https://graph.facebook.com/me/friends?limit=5000&access_token={token}"
    ).json()["summary"]["total_count"]
    return friends
  except:
    return None

###---------------### GET NAME ###--------------- ###


def scrape_name(token):
    name = reqg(
        f"https://graph.facebook.com/me?fields=name&access_token={token}"
    ).json()["name"]
    return name


###---------------### FACEBOOK BOT SHARE ###--------------- ###


def scrape_post_id(url):
    response = reqp("https://id.traodoisub.com/api.php", data={"link": url})
    scrapped_post_id = response.json().get("id")
    return scrapped_post_id


def scrape_facebook_token(cookie):
    headers = {
        "authority": "business.facebook.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "cache-control": "max-age=0",
        "cookie": cookie,
        "referer": "https://www.facebook.com/",
        "sec-ch-ua": '"Chromium";v="107", "Not=A?Brand";v="24"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }
    try:
        home_business = reqg(
            "https://business.facebook.com/content_management", headers=headers
        ).text
        token = home_business.split("EAAG")[1].split('","')[0]
        return f"{cookie}|EAAG{token}"
    except Exception as e:
        return None


def facebook_bot_share(cookie):
    post_url_to_share = input(f"Post URL (Facebook Lite): ")
    post_id = scrape_post_id(post_url_to_share)

    if not post_id:
        print("Invalid Post URL")
        exit()

    try:
        total_shares = int(input("Share Amount: "))
    except ValueError:
        print("Invalid Value")
        exit()

    token = scrape_facebook_token(cookie)
    if not token:
        print("Invalid cookie. Try fresh cookie.")
        exit()

    print("Post is sharing...")

    try:
        success_counter = [-1]
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate",
            "connection": "keep-alive",
            "content-length": "0",
            "cookie": cookie,
            "host": "graph.facebook.com",
            "user-agent": str(ua_generator.generate()),
        }

        for x in range(total_shares):
            response = reqp(
                f"https://graph.facebook.com/me/feed?link=https://m.facebook.com/{post_id}&published=0&access_token={token}",
                headers=headers,
            )
            scrapped_response = json.loads(response.text)
            share_success = scrapped_response["id"]

            if share_success:
                success_counter[-1] += 1
                AB = f"\r\r  [PROCESSING] - {success_counter[-1] + 1}/{total_shares} – {'{:.1%}'.format(success_counter[-1]/int(total_shares))}\r"
                print(f"{AB}", end="")
                sys.stdout.flush()
                cd(1)
            else:
                print(f"{scrapped_response}")

    except Exception as e:
        print(f"{scrapped_response}")
        print(f"TOTAL SHARES: {success_counter[-1]+1}/{total_shares}")
        exit()

    print(f"TOTAL SHARES: {success_counter[-1]+1}/{total_shares}")
    exit()

    return
