import math
from mysql_connect import MysqlConnect

class Contestant:

    def __init__(self, member, points, rating):
        self.member = member
        self.points = points
        self.rating = rating

class CodeforcesRatingCalculator:

    def __init__(self):
        self.db = MysqlConnect()
        self.db.connectDB()
        self.INITIAL_RATING = 1500
        self.contestants = list()
        self.records = dict()

    def getRecord(self, contestId):
        query_sql = "SELECT standings_id_" + str(contestId) + ".member, contestPoints, rating " \
                    "FROM standings_id_" + str(contestId) + ", registrants_id_" + str(contestId) + \
                    " WHERE standings_id_" + str(contestId) + ".member = registrants_id_" + str(contestId) + ".member"
        rst = self.db.query(query_sql)
        self.totParticipants = len(rst)
        for i in range(len(rst)):
            item = rst[i]
            self.contestants.append(Contestant(item[0], item[1], item[2]))

    def getEloWinProbability(self, Ra, Rb):
        return 1.0 / (1 + pow(10, (Rb-Ra)/400.0))

    def getSeed(self, rating):
        result = 1.0
        for other in self.contestants:
            result += self.getEloWinProbability(other.rating, rating)
        return result

    def getRatingToRank(self, rank):
        left, right = 1, 8000

        while right - left > 1:
            mid = (right + left) // 2
            if self.getSeed(mid) < rank:
                right = mid
            else:
                left = mid
        return left

    def reassignRank(self):
        self.contestants.sort(key=lambda item: item.points, reverse=True)

        idx = 0
        points = self.contestants[0].points
        i = 1
        while i < self.totParticipants:
            if self.contestants[i].points < points:
                j = idx
                while j < i:
                    self.contestants[j].rank = i
                    j += 1
                idx = i
                points = self.contestants[i].points
            i += 1
        j = idx
        while j < self.totParticipants:
            self.contestants[j].rank = self.totParticipants
            j += 1

    def process(self):

        if self.contestants == None:
            return

        # 重新计算 参赛者 rank
        self.reassignRank()

        for member in self.contestants:
            member.seed = 1.0
            for other in self.contestants:
                if member != other:
                    member.seed += self.getEloWinProbability(other.rating, member.rating)

        for contestant in self.contestants:
            midRank = math.sqrt(contestant.rank * contestant.seed)
            contestant.needRating = self.getRatingToRank(midRank)
            contestant.delta = (contestant.needRating - contestant.rating) // 2

        self.contestants.sort(key=lambda item:item.rating, reverse=True)

        # DO some adjuct
        # Total sum should not be more than ZERO.
        sum = 0

        # for contestant in self.contestants:
        #     print("%s %d %d" % (contestant.member, contestant.rating, contestant.delta) )

        for contestant in self.contestants:
            sum += contestant.delta
        inc = -(sum // self.totParticipants) - 1
        for contestant in self.contestants:
            contestant.delta += inc

        # Sum of top-4*sqrt should be adjusted to ZERO.
        sum = 0
        zeroSumCount = min(int(4*round(math.sqrt(self.totParticipants))), self.totParticipants)

        # for i in range(zeroSumCount):
        #     print("%s %d %d" % (self.contestants[i].member, self.contestants[i].rating, self.contestants[i].delta))

        for i in range(zeroSumCount):
            sum += self.contestants[i].delta
        inc = min(max(-(sum // zeroSumCount), -10), 0)
        for i in range(zeroSumCount):
            self.contestants[i].delta += inc

        self.validateDeltas()

    def validateDeltas(self):
        self.contestants.sort(key=lambda item:item.points, reverse=True)

        for i in range(self.totParticipants):
            for j in range(i+1, self.totParticipants):
                if self.contestants[i].rating > self.contestants[j].rating:
                    if self.contestants[i].rating + self.contestants[i].delta < self.contestants[j].rating + self.contestants[j].delta:
                        print("First rating invariant failed: %s vs. %s." % (self.contestants[i].member, self.contestants[j].member))

                if self.contestants[i].rating < self.contestants[j].rating:
                    if self.contestants[i].delta < self.contestants[j].delta:
                        print(1)
                        print("Second rating invariant failed: %s vs. %s." % (self.contestants[i].member, self.contestants[j].member))

    def prepareQuery(self):
        for contestant in self.contestants:
            self.records[contestant.member] = contestant

    def query(self, member):
        record = self.records[member]
        print("RatingChanges %d | Rating: %d -> %d" % (record.delta, record.rating, record.rating+record.delta))

    def printRecord(self):
        for i in range(20):
            self.query(self.contestants[i].member)

if __name__ == "__main__":

    sysCal = CodeforcesRatingCalculator()

    contestId = 790
    sysCal.getRecord(contestId)
    sysCal.process()
    sysCal.prepareQuery()
    sysCal.printRecord()

    while True:
        member = input("Please input the nickName: ")
        if member == "":
            break
        sysCal.query(member)