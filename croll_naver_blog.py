import requests
from bs4 import BeautifulSoup
import re
import datetime
import os


while True:
    url = input("URL을 입력하세요 : ")
    name = input("파일명을 입력하세요 (특수문자X) : ")

    num = url.split("/")[-1]

    target = "post-view" + num

    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")

    link = soup.find(id="mainFrame")["src"]

    url = "https://blog.naver.com" + link

    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")

    post = str(soup.find(id=target))

    lazy = "data-lazy-"

    post = re.sub(lazy, "", post, 0).strip()

    post = (
        """
    <style>
        body {
            margin: 0;
            padding-top: 5em;
            padding: 2em;
            text-align: left !important;
        }
    </style>
    """
        + post
    )

    now = datetime.datetime.now()

    nowDatetime = str(now.strftime("%Y-%m-%d-%H-%M"))

    save_name = f"{nowDatetime}_{name}.html"

    f = open(save_name, "w", encoding="utf8")

    f.write(post)

    f.close()

    print("작성 끝!")

    while True:
        open_now = input(f"{name}.html을 열까요? (Y/N/Q)")

        if open_now == "Y":
            os.system(save_name)
            os.system("exit()")
        elif open_now == "N":
            break
        elif open_now == "Q":
            print("프로그램을 종료합니다.")
            os.system("exit()")
        else:
            continue
