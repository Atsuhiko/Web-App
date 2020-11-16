import os
import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash


def select_all(con):
    """ SELECTする """
    cur = con.execute('select id, filepath, bad, happy, created from results order by id desc')
    return cur.fetchall()


def select(con, pk):
    """ 指定したキーのデータをSELECTする """
    cur = con.execute('select id, filepath, bad, happy, created from results where id=?', (pk,))
    return cur.fetchone()


def insert(con, filepath, bad, happy):
    """ INSERTする """
    cur = con.cursor()
    cur.execute('insert into results (filepath, bad, happy) values (?, ?, ?)', [filepath, bad, happy])
    pk = cur.lastrowid
    con.commit()
    return pk


def delete(con, pk):
    """ 指定したキーのデータをDELETEする """
    cur = con.cursor()
    cur.execute('delete from results where id=?', (pk,))
    con.commit()
