import pymysql.cursors

class MysqlConnect:

    def connectDB(self):
        # 获取数据库连接
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='codeforces_standings',
            charset='utf8mb4'
        )

    def closeDB(self):
        self.connection.close()

    def createTable(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except:
            self.connection.close()

    def insert(self, sql, value):
        try:
            # 获取会话指针
            with self.connection.cursor() as cursor:
                cursor.execute(sql, value)
                self.connection.commit()
        except Exception:
            self.connection.close()

    def query(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
                return cursor.fetchall()
        except Exception:
            self.connection.close()

    def update(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception:
            print(Exception.__traceback__)
            self.connection.close()

if __name__ == "__main__":

    db = MysqlConnect()
    db.connectDB()

    # TEST insert()
    # insert_sql = "INSERT INTO ratedList_Id_" + str(781) + "(idx, member, rating) VALUE (%s,%s,%s)"
    # value = ('1', "innocent_egg", str(1901))
    # db.insert(insert_sql, value)

    # TEST update()

    # TEST query()
    contestId = 786

    query_sql = "SELECT contestRank, standings_id_" + str(contestId) + ".member, rating " \
                "FROM standings_id_" + str(contestId) + ", registrants_id_" + str(contestId) + \
                " WHERE standings_id_" + str(contestId) + ".member = registrants_id_" + str(contestId) + ".member"
    rst = db.query(query_sql)


    print(rst)
    print(len(rst))
    # query_sql = "SELECT * FROM standings_id_" + str(contestId)
    # standings = db.query(query_sql)
    #
    # query_sql = "SELECT * FROM registrants_id_" + str(contestId)
    # registrants = db.query(query_sql)
    #
    # for record in range(standings):
