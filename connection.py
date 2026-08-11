import pymysql

def getConnection():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password="system25",
        database='library_management_project')
    return conn

def verifyMobile(mobile):
    if mobile.isdigit() and len(mobile) == 10 and mobile[0] in "6789":
        return True
    else:
        return False

def verifyEmail(email) :
    if len(email) > 5 and email.count('@') == 1 and email.count('.') >= 1:
        return True
    else:
        return False

