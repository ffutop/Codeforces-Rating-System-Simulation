import RatingSystem, CodeforcesRatingCal

def climbDataFromCF(contestId, pages):

    # 实例化 CodeforcesAPI 类
    codeforcesAPI = RatingSystem.CodeforcesAPI()

    # 获取 contest 最终排名
    codeforcesAPI.getCodeforcesStandings(contestId)
    # 获取注册参赛者的 oldRating
    codeforcesAPI.getCodefocesRegistrants(contestId, pages)

def calRating(contestId):

    # 实例化 CodeforcesRatingCalculator 类
    sysCal = CodeforcesRatingCal.CodeforcesRatingCalculator()

    # 从数据库获取对应 contest 记录
    sysCal.getRecord(contestId)
    # 处理数据
    sysCal.process()
    # 处理结果以 member.name 为 Key 做哈希 , 用于询问
    sysCal.prepareQuery()

    # This is writed for test
    sysCal.printRecord()

    while True:
        member = input("Please input the nickName: ")
        if member == "":
            break
        sysCal.query(member)

if __name__ == "__main__":
    # 获取需进行计算的 contest ID
    contestId = int(input("请输入 contestId: "))
    registered = int(input("请输入注册参赛者人数："))
    pages = (registered + 249) // 250

    climbDataFromCF(contestId, registered)

    calRating(contestId)