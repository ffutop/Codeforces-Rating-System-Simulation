import math
from mysql_connect import MysqlConnect

class Contestant:

    def __init__(self):
        self.member = 0
        self.rating = 0

    def __init__(self, member, rating):
        self.member = member
        self.rating = rating

class CodeforcesRatingCalculator:

    def __init__(self):
        self.db = MysqlConnect()
        self.db.connectDB()
        self.INITIAL_RATING = 1500
        self.oldRatings = dict()
        self.ranks = dict()
        self.deltas = dict()
        self.contestant = list()

    def getRecord(self, contestId):
        query_sql = "SELECT contestRank, standings_id_" + str(contestId) + ".member, rating " \
                    "FROM standings_id_" + str(contestId) + ", registrants_id_" + str(contestId) + \
                    " WHERE standings_id_" + str(contestId) + ".member = registrants_id_" + str(contestId) + ".member"
        rst = self.db.query(query_sql)
        self.totParticipants = len(rst)
        for i in range(len(rst)):
            item = rst[i]
            self.ranks[item[1]] = item[0]
            self.oldRatings[item[1]] = item[2]
            self.contestant.append(Contestant(item[1], item[2]))

    def getEloWinProbability(self, Ra, Rb):
        return 1.0 / (1 + pow(10, (Rb-Ra)/400.0))

    def getSeed(self, rating):
        result = 1.0
        for other in self.oldRatings:
            result += self.getEloWinProbability(self.oldRatings[other], rating)
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

    def process(self):

        for member in self.oldRatings:
            seed = 1.0
            rating = self.oldRatings[member]
            for other in self.oldRatings:
                if other == member:
                    continue
                else:
                    seed += self.getEloWinProbability(self.oldRatings[other], rating)
            minRank = math.sqrt(self.ranks[member] * seed)
            needRating = self.getRatingToRank(minRank)
            self.deltas[member] = (needRating - rating) / 2

        # DO some adjuct
        # Total sum should not be more than ZERO.
        sum = 0
        for member in self.deltas:
            sum += self.deltas[member]
        inc = -sum / self.totParticipants - 1
        for member in self.deltas:
            self.deltas[member] += inc

        # Sum of top-4*sqrt should be adjusted to ZERO.
        sum = 0
        zeroSumCount = min(4*round(math.sqrt(self.totParticipants)), self.totParticipants)
        self.contestant.sort(key=lambda contestant: contestant.rating, reverse=True)
        for i in range(zeroSumCount):
            sum += self.deltas[self.contestant[i].member]
        # for member in self.deltas:
        #     sum += self.deltas[member]
        inc = min(max(-sum / zeroSumCount, -10), 0)
        for i in range(zeroSumCount):
            self.deltas[self.contestant[i].member] += inc
        # for member in self.deltas:
        #     self.deltas[member] += inc

    def query(self, member):
        print("RatingChanges %d | Rating: %d -> %d" % (self.deltas[member], self.oldRatings[member], self.oldRatings[member] + self.deltas[member]))

if __name__ == "__main__":

    sysCal = CodeforcesRatingCalculator()

    contestId = 781
    sysCal.getRecord(contestId)
    sysCal.process()

    while True:
        member = input("Please input the nickName: ")
        if member == "":
            break
        sysCal.query(member)