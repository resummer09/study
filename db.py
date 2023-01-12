from datetime import datetime, timedelta
import pymysql

HOST = '127.0.0.1'
PORT = 3306
USER = 'user_t'
PASSWORD = 'sansio250'

# 연결 테스트
# conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db='yr_db', charset='utf8')
# if conn.open:
#     with conn.cursor() as curs:
#         print('connected')

def login(id:str, pw:str):
    print(f'@ 로그인 시도 [ID:{id}| PW:{pw}]')
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db='yr_db', charset='utf8')
    cur = conn.cursor()
    sql = f"SELECT 아이디, 비밀번호, 이름 FROM yr_db.members WHERE 아이디 = '{id}'"
    cur.execute(sql)
    member = cur.fetchone()
    conn.close()
    print(f'@ 조회된 DB : {member}')

    if member != None:
        if member[1] == pw :
            return True, '로그인 성공', member[2]
        else:
            return False, '- 비밀번호가 일치하지 않습니다.', None
    else:
        return False, '- 존재하지 않는 아이디입니다.', None

def today_attendance(user:str, today):
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db='yr_db', charset='utf8')
    cur = conn.cursor()
    sql = f"SELECT * FROM yr_db.attendance WHERE 이름 = '{user}' AND 훈련일자 = '{today}'"
    cur.execute(sql)
    data = cur.fetchone()

    if data == None :
        print('@ attendance 기록 INSERT')
        sql = f"INSERT INTO yr_db.attendance(훈련일자, 이름) VALUES('{today}', '{user}');"
        cur.execute(sql)
        conn.commit()
        sql = f"SELECT * FROM yr_db.attendance WHERE 이름 = '{user}' AND 훈련일자 = '{today}'"
        cur.execute(sql)
        data = cur.fetchone()

    conn.close()

    print(f'[{today} {user}] DB : {data}')
    return data

def timestamp(user:str, option:str, time, today):
    print(f'@ attendance 기록에 {option} UPDATE')
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db='yr_db', charset='utf8')
    cur = conn.cursor()
    sql = f"UPDATE yr_db.attendance SET {option} = '{time}' WHERE 이름 = '{user}' AND 훈련일자 = '{today}';"
    cur.execute(sql)
    conn.commit()
    conn.close()
    print(f'@ {option} 기록 완료')

# 출결 현황
def list_up_attendance(user:str, today:str):
    conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db='yr_db', charset='utf8')
    cur = conn.cursor()
    sql = f"SELECT 기록, COUNT(*) as 일수 FROM yr_db.attendance " \
          f"WHERE 이름 = '{user}' and 훈련일자 < '{today}' " \
          f"and 기록 IS NOT NULL" \
          f"GROUP BY 기록 ORDER BY 기록 DESC;"
    cur.execute(sql)
    rows = cur.fetchall()
    atten = {}
    for row in rows:
        atten[row[0]] = row[1]
    print(atten)
    conn.close()

