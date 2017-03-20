import requests
from bs4 import BeautifulSoup
from mysql_connect import MysqlConnect

class CodeforcesAPI:

    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
        self.baseStandingUrl = "http://codeforces.com/api/contest.standings?contestId="
        self.baseRegistrantsUrl = "http://codeforces.com/contestRegistrants/"
        self.db = MysqlConnect()
        self.db.connectDB()

    def __del__(self):
        self.db.closeDB()

    def getCodeforcesStandings(self, contestId):

        create_table_sql = "CREATE TABLE IF NOT EXISTS standings_Id_" + str(contestId)  \
            + "(idx INTEGER ,\
              contestId INTEGER ,\
              contestRank INTEGER ,\
              contestPoints INTEGER ,\
              member VARCHAR (255),\
              oldRating INTEGER ,\
              ratingChange INTEGER ,\
              newRating INTEGER )"

        self.db.createTable(create_table_sql)

        url = self.baseStandingUrl + str(contestId)
        # requests 获取网页对象
        cf_standings = requests.get(url, headers=self.headers)
        # 对其 JSON 格式进行解析
        cf_standings_json = cf_standings.json()
        cf_standings_result = cf_standings_json["result"]["rows"]

        insert_sql = "INSERT INTO standings_Id_" + str(contestId) + "(idx, contestId, contestRank, contestPoints, member) VALUES (%s,%s,%s,%s,%s)"

        for idx in range(len(cf_standings_result)):
            item = cf_standings_result[idx]
            value = (str(idx), contestId, item["rank"], item["points"], item["party"]["members"][0]["handle"])
            self.db.insert(insert_sql, value)

    def getCodeforcesRatedList(self, contestId):

        url = self.baseRatingUrl

        cf_ratedList = requests.get(url, headers=self.headers)

        cf_ratedList_json = cf_ratedList.json()
        insert_sql = "INSERT INTO ratedList_Id_" + str(contestId) + "(idx, member, rating) VALUES (%s,%s,%s)"
        for idx in range(len(cf_ratedList_json)):
            item = cf_ratedList_json[idx]
            value = (str(idx), item["handle"], item["rank"], item["rating"])
            self.db.insert(insert_sql, value)

    def getCodefocesRegistrants(self, contestId, pages):

        create_table_sql = "CREATE TABLE IF NOT EXISTS registrants_Id_" + str(contestId) \
                           + "(idx INTEGER ,\
                      member VARCHAR (255),\
                      rating INTEGER )"
        self.db.createTable(create_table_sql)

        baseUrl = self.baseRegistrantsUrl + str(contestId) + "/page/";

        insert_sql = "INSERT INTO registrants_Id_" + str(contestId) + "(idx, member, rating) VALUES (%s,%s,%s)"

        for page in range(1, pages+1):
            url = baseUrl + str(page)
            web_data = requests.get(url, self.headers)
            soup = BeautifulSoup(web_data.text, "lxml", from_encoding='utf-8')
            # registrantsIdxP = soup.select("table > tr > td")
            # registrantsIdx = registrantsIdxP.get_text()
            # # registrantsIdx = soup.find_all('td', class_='left').get_text()
            # membersP = soup.find_all('a', class_='user-violet')
            # members = membersP.text()
            # # members = soup.find_all('a', class_='user-violet').get_text()
            # ratingsP = soup.select("table > tr > td")
            # ratings = ratingsP.get_text()
            # ratings = soup.find_all('td', class_='right').get_text()

            tds = soup.select("table > tr > td")

            i = 0
            while i < len(tds):
                value = (int(tds[i].get_text().strip()), tds[i+1].get_text().strip(), float(tds[i+2].get_text().strip()))
                i += 3
                self.db.insert(insert_sql, value)

            # for value in zip(registrantsIdx, members, ratings):
            #     self.db.insert(insert_sql, value)


    # def updateStandings(self, contestId):


        # update_sql = "UPDATE standings_Id_" + str(contestId) + " set oldRating = " + mp[""] + " where member = " +


if __name__ == "__main__":

    codeforcesAPI = CodeforcesAPI()

    contestId = int(input("请输入 contestId："))
    pages = int(input("请输入注册参赛者的人数："))
    pages = (pages + 249) // 250

    # codeforcesAPI.getCodeforcesRatedList(contestId)
    # 获取 contest 最终排名
    # codeforcesAPI.getCodeforcesStandings(contestId)
    # 获取注册参赛者的 oldRating
    codeforcesAPI.getCodefocesRegistrants(contestId, pages)