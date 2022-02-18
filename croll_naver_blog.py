import requests
from bs4 import BeautifulSoup
import re
import datetime
import os


while True:
    url = input("URL을 입력하세요 : ")
    name = input("파일명을 입력하세요 (특수문자X) : ")

    # 포스팅 일련번호
    num = url.split("/")[-1]

    # div id
    target = "post-view" + num

    # first croll
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # croll iframe src
    link = soup.find(id="mainFrame")["src"]

    # second croll
    url = "https://blog.naver.com" + link
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    # croll post content
    post = str(soup.find(id=target))

    # remove lazy img
    lazy = "data-lazy-"
    post = re.sub(lazy, "", post, 0).strip()

    # add design
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

    # now time
    now = datetime.datetime.now()
    nowDatetime = str(now.strftime("%Y-%m-%d-%H-%M"))

    # save name
    save_name = f"{nowDatetime}_{name}.html"

    # write file
    f = open(save_name, "w", encoding="utf8")
    f.write(post)
    f.close()
    print("작성 끝!")

    # next act
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
