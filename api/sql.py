from typing import Optional
from link import *
from flask import flash

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    def execute_input(cursor, input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()



class Member():
    def get_member(account):
        sql = "SELECT ACCOUNT, PASSWORD, MID, IDENTITY, NAME FROM MEMBER WHERE ACCOUNT = :id"
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'id' : account}))
    
    def get_all_account():
        sql = "SELECT ACCOUNT FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))

    def create_member(input):
        sql = 'INSERT INTO MEMBER VALUES (null, :name, :account, :password, :identity)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(tno, pid):
        sql = 'DELETE FROM RECORD WHERE TNO=:tno and PID=:pid '
        DB.execute_input(DB.prepare(sql), {'tno': tno, 'pid':pid})
        DB.commit()
        
    def get_order(userid):
        sql = 'SELECT * FROM ORDER_LIST WHERE MID = :id ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':userid}))
    
    def get_role(userid):
        sql = 'SELECT IDENTITY, NAME FROM MEMBER WHERE MID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()
       
class Product():
    def count():
        sql = 'SELECT COUNT(*) FROM VIDEOS'
        return DB.fetchone(DB.execute( DB.connect(), sql))
    
    def get_product(pid):
        sql ='SELECT * FROM VIDEOS WHERE VID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))

    def get_all_product():
        sql = 'SELECT * FROM VIDEOS'
        return DB.fetchall(DB.execute( DB.connect(), sql))
    
    def get_name(pid):
        sql = 'SELECT TITLE FROM VIDEOS WHERE PID = :id'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':pid}))[0]

    def get_name_exist(name):
        sql = 'SELECT count(*) FROM VIDEOS WHERE TITLE = :name'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'name':name}))[0]

    def add_product(input):
        sql = 'INSERT INTO VIDEOS (vID, title, upload_date, classify, link) VALUES (:pid, :name, :price, :category, :description)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_product(pid):
        sql = 'DELETE FROM VIDEOS WHERE VID = :id '
        DB.execute_input(DB.prepare(sql), {'id': pid})
        DB.commit()

    def update_product(input):
        sql = 'UPDATE VIDEOS SET TITLE=:name, UPLOAD_DATE=:price, CLASSIFY=:category, LINK=:description WHERE VID=:pid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_product(pid, tno):
        sql = 'SELECT * FROM RECORD WHERE PID = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid, 'tno':tno}))

    def get_price(pid):
        sql = 'SELECT PRICE FROM PRODUCT WHERE PID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': pid}))[0]

    def add_product(input):
        sql = 'INSERT INTO RECORD VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, pid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and PID=:pid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'pid':pid}) )[0]
    
    def update_product(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE PID=:pid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(pid):
        sql = 'SELECT * FROM RECORD WHERE PID=:pid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'pid':pid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]
    

class Order_List():
    def add_order(input):
        sql = 'INSERT INTO ORDER_LIST VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_order():
        sql = 'SELECT OID, NAME, PRICE, ORDERTIME FROM ORDER_LIST NATURAL JOIN MEMBER ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, P.PNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_LIST O, RECORD R, PRODUCT P WHERE O.TNO = R.TNO AND R.PID = P.PID'
        return DB.fetchall(DB.execute(DB.connect(), sql))


class Analysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), SUM(PRICE) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i}))

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), COUNT(OID) FROM ORDER_LIST WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))
    
    def category_sale():
        sql = 'SELECT SUM(TOTAL), CATEGORY FROM(SELECT * FROM PRODUCT,RECORD WHERE PRODUCT.PID = RECORD.PID) GROUP BY CATEGORY'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT SUM(PRICE), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY SUM(PRICE) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.NAME FROM ORDER_LIST, MEMBER WHERE ORDER_LIST.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.NAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

class Transaction():
    def __init__(self, pid, user_id, mid, timestamp):
        self.pid = pid
        self.user_id = user_id
        self.mid = mid
        self.timestamp = timestamp

    def save(self):
        sql = 'INSERT INTO GROUP10.TRANSACTIONS (TID, TRANSACTION_DATE, BUY_ID, mID) VALUES (TID_INCREASE.NEXTVAL, :timestamp, :pid, :mid)'
        DB.execute_input(DB.prepare(sql), {'timestamp': self.timestamp, 'pid': self.pid, 'mid': self.mid})
        DB.commit()

    def check_purchase(pid, mid):
        sql = 'SELECT count(*) FROM transactions WHERE buy_id = :pid AND mid = :mid'
#        flash(f"SQL:{sql},pid: {pid},mid: {mid}")
        sql = '''
        SELECT count(*)
        FROM transactions
        WHERE (buy_id = :pid AND mid = :mid)
           OR (buy_id IN (SELECT pID FROM contain WHERE vids LIKE '%' || :pid || '%') AND mid = :mid)
        '''
        result = DB.execute_input(DB.prepare(sql), {'pid': pid, 'mid': mid})
        count = DB.fetchall(result)
#        flash(f"count: {count}")
        return count

    def get_user_purchases(mid):
        sql = '''
        SELECT t.tid, v.vId, v.title, v.upload_date, p.pId, p.title as plan_title,t.TRANSACTION_DATE
FROM GROUP10.TRANSACTIONS t
LEFT JOIN GROUP10.VIDEOS v ON v.vId = t.BUY_ID AND t.BUY_ID LIKE 'v%'
LEFT JOIN GROUP10.PLANS p ON p.pId = t.BUY_ID AND t.BUY_ID NOT LIKE 'v%'
where mid = :mid
        '''
        result = DB.execute_input(DB.prepare(sql), {'mid': mid})
        purchases = DB.fetchall(result)
        flash(f"purchases: {purchases}")
        return purchases

    def delete_by_tid(tid):
        sql = 'DELETE FROM transactions WHERE tid = :tid'
        DB.execute_input(DB.prepare(sql), {'tid': tid})
        DB.commit()

class Plan():
    def get_all_plans():
        sql = 'SELECT * FROM Plans'
        plans = DB.fetchall(DB.execute(DB.connect(), sql))
        return plans

    def get_videos_by_plan(pid):
        sql = 'SELECT vIDs FROM Contain WHERE pID = :pid'
        result = DB.execute_input(DB.prepare(sql), {'pid': pid})
        video_ids = DB.fetchall(result)
        return video_ids


