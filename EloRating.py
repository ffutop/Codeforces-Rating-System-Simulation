"""
This .py was Abandoned. CAUSE the Codeforces Platform modified the rating system.
"""

# from mysql_connect import MysqlConnect
#
# class EloRating:
#
#     def __init__(self):
#         self.db = MysqlConnect()
#         self.db.connectDB()
#         self.rank = dict()
#         self.oldRating = dict()
#
#     def getRecord(self, contestId):
#         query_sql = "SELECT contestRank, standings_id_" + str(contestId) + ".member, rating " \
#                     "FROM standings_id_" + str(contestId) + ", registrants_id_" + str(contestId) + \
#                     " WHERE standings_id_" + str(contestId) + ".member = registrants_id_" + str(contestId) + ".member"
#         rst = self.db.query(query_sql)
#         self.totParticipants = len(rst)
#         for i in range(len(rst)):
#             item = rst[i]
#             self.rank[item[1]] = item[0]
#             self.oldRating[item[1]] = item[2]
#
#     def E(self, Ra, Rb):
#         Qa = pow(10, Ra/400)
#         Qb = pow(10, Rb/400)
#         Ea = Qa / (Qa + Qb)
#         return Ea
#
#     def calRatingChange(self, member):
#         memRank = self.rank[member]
#         memOldRating = self.oldRating[member]
#         Sa = 0.0
#         for key in self.rank:
#             if key == member:
#                 continue
#             if self.rank[key] > memRank:
#                 Sa += 1.0
#             elif self.rank[key] == memRank:
#                 Sa += 0.5
#             else:
#                 Sa += 0.0
#         Seeda = 1.0
#         for key in self.oldRating:
#             if key == member:
#                 continue
#             Seeda += self.E(self.oldRating[key], memOldRating)
#             # Ea += self.E(memOldRating, self.oldRating[key])
#         print(Seeda)
#
#         # K = 16
#         # ratingChange = (Sa - Ea)
#         # print(ratingChange)
#
# if __name__ == "__main__":
#
#     eloRating = EloRating()
#
#     contestId = 781
#     eloRating.getRecord(contestId)
#
#     while True:
#         member = input("Please input the nickName: ")
#         if member == "":
#             break
#         eloRating.calRatingChange(member)
#
#
