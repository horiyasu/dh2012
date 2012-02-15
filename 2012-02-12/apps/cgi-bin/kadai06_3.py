#!/Users/horiuchi/.virtualenvs/dh2012/bin/python
# -*- coding: utf-8 -*-

"""
CREATE DATABASE dh2012 DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
CREATE table session(
  id int not null auto_increment primary key,
  session_id varchar(255) unique,
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
        fruits_in_basket = []
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
    sql = "SELECT data FROM " + table_name + " WHERE session_id=%s"
    cur = con.cursor()
    cur.execute(sql, (session_id, ))
    res = cur.fetchone()
    if res is None:
        return []
    else:
        return json.loads(res[0])

def save_fruits(con, table_name, session_id, fruits_list):
    """
    フルーツを保存する
    Arguments:
    - `con`:
    - `table_name`:
    - `session_id`:
    - `fruits_list`:
    """
    fruits_str = json.dumps(fruits_list)
    sql = "SELECT data FROM " + table_name + " WHERE session_id=%s"
    cur = con.cursor()
    cur.execute(sql, (session_id, ))
    res = cur.fetchone()
    if res is None:
        save_sql = "INSERT INTO " + table_name + "  (data,session_id) VALUES(%s,%s)"
    else:
        save_sql = "UPDATE " + table_name + " SET data=%s WHERE session_id=%s"
    cur.execute(save_sql, (fruits_str,session_id))
    con.commit()

def clear_fruits(con, table_name, session_id):
    """
    フルーツをクリアする
    Arguments:
    - `con`:
    - `table_name`:
    - `session_id`:
    """
    sql = "DELETE FROM " + table_name + " WHERE session_id=%s"
    cur = con.cursor()
    cur.execute(sql, (session_id, ))
    con.commit()
    
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
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), TEMPLATE_DIR, 'index.html'))
    f = open(path,'r').read()
    base_to_html(cookie)

    added_str = "と".join([ FRUITS[fruit] for fruit in choose_list ])
    if added_str:
        added_str += "を追加しました。"

    message_str = "<br />".join(message_list)

    fruits_dict = {}
    for fruit in fruits_in_basket:
        if fruit in fruits_dict:
            fruits_dict[fruit] += 1
        else:
            fruits_dict[fruit] = 1
    fruits_in_basket_list = []
    for name,count in fruits_dict.items():
        fruits_in_basket_list.append("%s x %d" % (FRUITS[name], count))

    fruits_in_basket_str = '<br />'.join(fruits_in_basket_list)

    print f % (added_str, message_str, fruits_in_basket_str)

main()
