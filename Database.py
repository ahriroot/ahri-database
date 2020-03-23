import time
import random
import string
import pymysql
import pymongo


class Connect:
    server = 'db.ahriknow.com'
    mysql_password = 'Aa12345.'
    mongo_password = 'Aa12345.'
    mongo = f'mongodb://root:{mongo_password}@{server}:27017/'

    def get_dbs(self, t, user):
        if t == 'mongo':
            conn = pymongo.MongoClient(self.mongo)
            dbs = conn['logs']['dbinfo'].find({'user': user})
            result = list()
            for i in dbs:
                i['_id'] = str(i['_id'])
                result.append(i)
            return result
        elif t == 'mysql':
            mysql = pymysql.connect(host=self.server, user="root", password=self.mysql_password, port=3306,
                                    charset='utf8')
            cursor = mysql.cursor()
            cursor.execute(f"select * from `logs`.`dbinfo` where `user`='{user}'")
            dbs = cursor.fetchall()
            cursor.close()
            mysql.close()
            result = list()
            for i in dbs:
                result.append(i)
            return result

    def create(self, t, db, name, password=None):
        if t == 'mongo':
            conn = pymongo.MongoClient(self.mongo)
            info = {
                'date': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'database': db,
                'username': name,
                'password': password,
                'user': ''
            }
            conn['logs']['dbinfo'].insert_one(info)
            conn[db]['version'].insert_one(info)
            result = conn[db].command('createUser', name, pwd=password, roles=["dbAdmin"])
            return True if 'ok' in result else False
        elif t == 'mysql':
            mysql = pymysql.connect(host=self.server, user="root", password=self.mysql_password, port=3306,
                                    charset='utf8')
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cursor = mysql.cursor()
            cursor.execute(f'create database `{db}` default charset utf8mb4 collate utf8mb4_unicode_ci')
            cursor.execute(f'create user `{name}`@`%` identified by \'{password}\'')
            cursor.execute(f'grant all on `{db}`.* to `{name}`@`%`')
            cursor.execute(f'use `logs`')
            cursor.execute(
                f"insert into `dbinfo`(`date`, `database`, `username`, `password`, `user`) values ('{date}', '{db}', '{name}', '{password}', 'none')")
            mysql.commit()
            cursor.close()
            mysql.close()
            return True

    def drop(self, t, db):
        if t == 'mongo':
            conn = pymongo.MongoClient(self.mongo)
            users = conn['logs']['dbinfo'].find({'database': db})
            for i in users:
                conn[db].command('dropUser', i['username'])
            conn.drop_database(db)
            conn['logs']['dbinfo'].delete_many({'database': db})
            return True
        elif t == 'mysql':
            mysql = pymysql.connect(host=self.server, user="root", password=self.mysql_password, port=3306,
                                    charset='utf8')
            cursor = mysql.cursor()
            cursor.execute('select distinct CONCAT(user) as query from mysql.user')
            res = cursor.fetchall()
            cursor.execute('select distinct CONCAT(username) as query from logs.dbinfo')
            users = cursor.fetchall()
            for i in users:
                if i in res:
                    cursor.execute(f'revoke all on `{db}`.* from `{i[0]}`@`%`')
                    cursor.execute(f'drop user if exists `{i[0]}`@`%`')
            cursor.execute(f'drop database if exists `{db}`')
            cursor.execute(f"delete from `logs`.`dbinfo` where `database`='{db}'")
            mysql.commit()
            cursor.close()
            mysql.close()

    def id_generator(self, size=12, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
