import time
from flask import Flask
from flask import request
# from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import ssl
import json
import ecdsa
import hashlib
import secrets
import asn1tools
import base64
import binascii
import pymysql

app = Flask(__name__)


@app.route('/api/queue/<string:imsi>')
def retrieve_from_queue(imsi):
    return retrieve_From_Queue(imsi)


@app.route('/api/db/table/<string:tablename>')
def all_table(tablename):
    return log_All(tablename)


@app.route('/api/db/columns/<string:tablename>')
def columns(tablename):
    return get_Columns(tablename)


@app.route('/api/db/adduser', methods=['POST'])
def add_user():
    obj = request.get_json()
    # if not request.form['imsi'] or not request.form['msisdn'] or not request.form['imei']:
    if 'imsi' not in obj or 'msisdn' not in obj or 'imei' not in obj or 'sqn' not in obj or 'rand' not in obj or 'active' not in obj:
        print('missing arguments')
        return "error"
    return add_User(obj['imsi'], obj['msisdn'], obj['imei'], obj['active'], obj['sqn'], obj['rand'])


@app.route('/api/db/deleteuser', methods=['POST'])
def delete_user():
    obj = request.get_json()
    # if not request.form['imsi'] or not request.form['msisdn'] or not request.form['imei']:
    if 'imsi' not in obj:
        print('missing arguments')
        return "error"
    return delete_User(obj['imsi'])


@app.route('/api/db/updateuser', methods=['POST'])
def update_user():
    obj = request.get_json()
    if 'imsi' not in obj:
        print('missing imsi')
        return "error"
    imsi = obj['imsi']
    imei = obj['imei'] if 'imei' in obj else ''
    active = obj['active'] if 'active' in obj else ''
    return update_User(imsi, imei, active)


def connect_to_db():
    return pymysql.connect("localhost", "root", "asddfdlxx", "esim")


def log_All(tablename):
    tableData = []
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # columns = get_Columns('users')
            # query = ''
            # for col in columns:
            # query += "\'%s\', %s, " % (col, col)
            # cursor.execute("SELECT JSON_ARRAYAGG(JSON_OBJECT(%s)) from users" % query)
            if(tablename not in ['users', 'pdn']):
                raise Exception("nonexistent tablename")
            cursor.execute("SELECT * from %s" % tablename)
            results = cursor.fetchall()
            for i in range(len(results)):
                tableData.append([])
                for col in results[i]:
                    tableData[i].append(str(col))
    finally:
        connection.close()
    return json.dumps(tableData)


def get_Columns(tablename):
    columns = []
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            if(tablename not in ['users', 'pdn']):
                raise Exception("nonexistent tablename")
            cursor.execute("SHOW COLUMNS FROM %s" % tablename)
            results = cursor.fetchall()
            for row in results:
                columns.append(row[0])
            # converted_list = [str(element) for element in columns]
            # columns = ",".join(converted_list)
    finally:
        connection.close()
    return json.dumps(columns)


def add_User(imsi, msisdn, imei, active, sqn, rand):
    connection = connect_to_db()
    failed = False
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO `users` (`imsi`, `msisdn`, `imei`, `active`, `sqn`, `rand`) VALUES (%s, %s, %s, %s, %s, %s)", (imsi, msisdn, imei, active, sqn, rand))
        connection.commit()
    except Exception as inst:
        print('type of exception:')
        print(type(inst))
        print('exception text:')
        print(inst)
        failed = True
    finally:
        connection.close()
    return 'error' if failed else 'success'


def delete_User(imsi):
    connection = connect_to_db()
    failed = False
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM `users` WHERE `imsi` = %s", (imsi,))
        connection.commit()
    except Exception as inst:
        print('type of exception:')
        print(type(inst))
        print('exception text:')
        print(inst)
        failed = True
    finally:
        connection.close()
    return 'error' if failed else 'success'


def update_User(imsi, newImei, newActive):
    connection = connect_to_db()
    failed = False
    try:
        with connection.cursor() as cursor:
            if newImei or newActive:
                if not newImei:
                    cursor.execute(
                        "UPDATE `users` SET `active` = %s WHERE `imsi` = %s", (newActive, imsi))
                elif not newActive:
                    cursor.execute(
                        "UPDATE `users` SET `imei` = %s WHERE `imsi` = %s", (newImei, imsi))
                else:
                    cursor.execute(
                        "UPDATE `users` SET `imei` = %s, `active` = %s WHERE `imsi` = %s", (newImei, newActive, imsi))
        connection.commit()
    except Exception as inst:
        print('type of exception:')
        print(type(inst))
        print('exception text:')
        print(inst)
        failed = True
    finally:
        connection.close()
    return 'error' if failed else 'success'


# retrieve related updates from db
# send delete if imsi not in db's queue table
def retrieve_from_Queue(imsi):
    connection = connect_to_db()
    tableData = [[]]
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT `instruction` FROM `queue` WHERE `imsi` = %s", (imsi))
            results = cursor.fetchall()
            for i in range(len(results)):
                tableData.append([])
                for col in results[i]:
                    tableData[i].append(str(col))
    finally:
        connection.close()
    return json.dumps(tableData)
