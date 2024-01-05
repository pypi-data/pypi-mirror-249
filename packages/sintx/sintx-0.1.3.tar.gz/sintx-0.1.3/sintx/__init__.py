import os, json
from os import system as sintx

try:
    import requests
except ModuleNotFoundError:
    sintx("pip install requests")
    import requests

from requests import get as reqg
from requests import post as reqp
from requests import session as reqs

try:
    import bs4
except ModuleNotFoundError:
    sintx("pip install bs4")
    import bs4

from bs4 import BeautifulSoup as _sinsBs
from bs4 import BeautifulSoup as parser
from bs4 import BeautifulSoup as bs

try:
    import ua_generator
except ModuleNotFoundError:
    sintx("pip3 install -U ua-generator")
    import ua_generator

###---------------### COLORS ###--------------- ###

#sintx_blue = "\033[94m"
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
    followers = reqg(
        f"https://graph.facebook.com/me/subscribers?limit=1000&access_token={token}"
    ).json()["summary"]["total_count"]
    return followers


###---------------### GET FRIENDS ###--------------- ###


def scrape_friends(token):
    friends = reqg(
        f"https://graph.facebook.com/me/subscribers?limit=1000&access_token={token}"
    ).json()["summary"]["total_count"]
    return friends


###---------------### GET NAME ###--------------- ###


def scrape_name(token):
    name = reqg(
        f"https://graph.facebook.com/me?fields=name&access_token={token}"
    ).json()["name"]
    return name


