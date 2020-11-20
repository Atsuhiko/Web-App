import os
import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash


# SELECTする
def select_all(con):
    cur = con.execute('select id, filepath, bad, happy, created from results order by id desc')
    return cur.fetchall() # クエリ実行結果をすべて取得

# 指定したキーのデータをSELECTする
def select(con, pk):
    cur = con.execute('select id, filepath, bad, happy, created from results where id=?', (pk,))
    return cur.fetchone() # クエリ実行結果を一行取得

# INSERTする
def insert(con, filepath, bad, happy):
    cur = con.cursor() # カーソルオブジェクト
    cur.execute('insert into results (filepath, bad, happy) values (?, ?, ?)', [filepath, bad, happy])
    pk = cur.lastrowid # 最後似登録した行を取得
    con.commit() # 変更の反映
    return pk

# 指定したキーのデータをDELETEする
def delete(con, pk):
    cur = con.cursor() # カーソルオブジェクト
    cur.execute('delete from results where id=?', (pk,))
    con.commit() # 変更の反映
