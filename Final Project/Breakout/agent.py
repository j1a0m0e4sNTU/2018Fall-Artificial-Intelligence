import random

class Agent:
    def __init__(self):
        self.allData = None
        self.bricksInfo = None
        # boundary
        self.top = 10000
        self.bottom = 0
        self.ballDirection = (0, 0)
        self.lastBallPos = (0, 0)
        self.fallPointX = 0

    def observe(self, rawInfo):
        allData = rawInfo.split()
        allData = [int(data) for data in allData]
        self.allData = allData
        self.bricksInfo = self.getBricksInfo()
        
        self.updateBoundary()
        self.computeBallDirection()
        self.predictFallPoint()
    
    def updateBoundary(self):
        _, ballY = self.getBallCenter()
        self.top = min(self.top, ballY)
        self.bottom = max(self.bottom, ballY)

    def computeBallDirection(self):
        ballx, bally = self.getBallCenter()
        lastBallx, lastBally = self.lastBallPos
        self.ballDirection = (ballx - lastBallx, bally - lastBally)
        self.lastBallPos = (ballx, bally)

    def predictFallPoint(self):
        vecX, vecY = self.ballDirection
        ballX, ballY = self.getBallCenter()       
        if vecY == 0 :
            return
        elif vecY > 0: 
            factor = (self.bottom - ballY) / vecY
            self.fallPointX = ballX + factor*vecX
        else: # ball is moving upwards
            height = self.bottom - self.top
            factor = (height + ballY) / (-vecY)
            self.fallPointX = ballX + factor*vecX

    def getBallCenter(self):
        center = (self.allData[0], self.allData[1])
        return center
    
    def getPaddleCenterX(self):
        return self.allData[2]

    def getPaddleWidth(self):
        return self.allData[3]

    def getLives(self):
        return self.allData[4]

    def getScore(self):
        return self.allData[5]

    def isRight(self, pos):
        return pos[0] > self.getPaddleCenterX() 
    
    def isLeft(self, pos):
        return pos[0] < self.getPaddleCenterX() 
    
    def inPaddleWidth(self, pos):
        paddleX = self.getPaddleCenterX()
        paddleWidth = self.getPaddleWidth()
        return paddleX - paddleWidth/3 <= pos[0] <= paddleX + paddleWidth/3
    
    def getBricksInfo(self):
        rawBricksInfo = self.allData[6:]
        bricksNum = len(rawBricksInfo)//3
        bricksInfo = []
        for i in range(bricksNum):
            centerx = rawBricksInfo[3*i + 0]
            centery = rawBricksInfo[3*i + 1]
            colorIdx= rawBricksInfo[3*i + 2]
            info = (centerx, centery, colorIdx)
            bricksInfo.append(info)
        return bricksInfo

    def randomPolicy(self):
        if random.random() > 0.5:
            return 1
        else:
            return -1

    def simplePolicy(self):
        if self.isRight(self.getBallCenter()):
            return 1
        elif self.isLeft(self.getBallCenter()):
            return -1
        else:
            return 0

    def policy_A(self):
        fallPoint = (self.fallPointX, self.bottom)
        if self.inPaddleWidth(fallPoint):
            return 0
        elif self.isRight(fallPoint):
            return 1
        elif self.isLeft(fallPoint):
            return -1
        else :
            return 0
    
    def policy_B(self):
        ballPos = self.getBallCenter()
        if self.inPaddleWidth(ballPos):
            return 0
        elif self.isRight(ballPos):
            return 1
        elif self.isLeft(ballPos):
            return -1
        else :
            return 0

    def policy_C(self):
        if self.ballDirection[1] < 0:
            return self.simplePolicy()
        else:
            return self.policy_A()

    def makeDecision(self):
        return self.policy_C()
        

###############  Decision #################

agent = Agent()
def decide(instr):
    agent.observe(instr)
    decision = agent.makeDecision()
    #print(decision)
    return decision

