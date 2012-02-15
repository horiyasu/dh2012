#!/Users/horiuchi/.virtualenvs/dh2012/bin/python
# -*- coding: utf-8 -*-

"""
CREATE DATABASE dh2012 DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE table session(
  id int not null auto_increment primary key,
  session_id varchar(20) unique,
  data text
);

session_idはユニーク、dataにはjson形式のデータを保存
"""

import os
import cgi
import cgitb; cgitb.enable()
from Cookie import SimpleCookie
from random import seed, randint
import json
import MySQLdb

DBHOST = "localhost"
DBNAME = "dh2012"
DBUSER = "root"
DBPASSWD = ""

TABLE_NAME = 'session'

TEMPLATE_DIR = "../../templates/"

EMPTY_MESSAGE = "かごの中にはまだ何も入っていません。"
ERROR_MESSAGE = "不正なセッションIDです。"
CLEAR_MESSAGE = "かごの中が空になりました。"

FRUITS = {
    "apple": "りんご",
    "orange": "みかん",
    "grape": "ぶどう",
}

def main():
    con = MySQLdb.connect(host=DBHOST, db=DBNAME, user=DBUSER, passwd=DBPASSWD)
    form = cgi.FieldStorage()
    cookie = SimpleCookie(os.environ.get("HTTP_COOKIE",""))

    # セッションIDを取得
    session_id = get_session_id(cookie)

    # フルーツデータを取得
    fruits_in_basket = get_fruits(con, TABLE_NAME, session_id)

    message_list = []
    choose_list = []

    which = form.getvalue("which",None)
    if which == "add": # 買い物かごにデータを追加
        choose_list = form.getlist("fruits")
        fruits_in_basket += choose_list
        save_fruits(con, TABLE_NAME, session_id, fruits_in_basket)
        
    elif which == "clear": # かごの中を空にする
        clear_fruits(con, TABLE_NAME, session_id)
        message_list.append(CLEAR_MESSAGE)

    if fruits_in_basket == []:
        message_list.append(EMPTY_MESSAGE)

    show_html(fruits_in_basket, choose_list, message_list, cookie)
    con.close()

# セッションIDを発行する。
def generate_sid():
     generated = ""
     seed()
     for i in range(20):
          generated += str(randint(1,100))
     return generated

# セッションIDをクッキーから取得する
def get_session_id(cookie):
    if not cookie.has_key('sid'):
        cookie["sid"] = generate_sid()
    session_id = cookie["sid"].value
    return session_id

def get_fruits(con, table_name, session_id):
    """
    フルーツを取得する
    Arguments:
    - `con`:
    - `table_name`:
    - `session_id`:
    """
    pass

def save_fruits(con, table_name, session_id, fruits_list):
    """
    フルーツを保存する
    Arguments:
    - `con`:
    - `table_name`:
    - `session_id`:
    - `fruits_list`:
    """
    pass

def clear_fruits(con, table_name, session_id):
    """
    フルーツをクリアする
    Arguments:
    - `con`:
    - `table_name`:
    - `session_id`:
    """
    pass
    

#htmlを表示するためのベース
def base_to_html(cookie=None):
     print "Content-type:text/html; charset=utf-8"
     if cookie is not None:
          print cookie.output()
     print ""

def show_html(fruits_in_basket, choose_list, message_list, cookie):
    """
    HTMLをprintする
    Arguments:
    - `fruits_in_basket`:
    - `choose_list`:
    - `message_list`:
    - `cookie`:
    """
    path = "%s/%s" % (TEMPLATE_DIR, 'index.html')
    f = open(path,'r').read()
    base_to_html(cookie)
    fruits_in_basket_str = ""
    added_str = ""
    message_str = ""
    print f % (added_str, message_str, fruits_in_basket_str)

main()
