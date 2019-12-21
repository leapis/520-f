import numpy as np
import random
import time

class State:

    SHEEP   = 0
    WOLF    = 1    

    WOLFB_R = -8
    WOLFR_R = -4
    SHEEP_R = -5

    def __init__(self, dim, sheep=None, wolfB=None, wolfR=None):
        self.turn = State.WOLF
        self.grid = np.zeros((dim, dim), dtype=int)
        self.dim = dim
        dim = dim - 1
        self.sheep = sheep or (random.randint(0,dim), random.randint(0,dim))
        self.wolfB = wolfB
        self.wolfR = wolfR
        if not self.wolfB:
            while (self.wolfB == None or self.wolfB == self.sheep):
                self.wolfB = (random.randint(0,dim), random.randint(0,dim))
        if not self.wolfR:
            while (self.wolfR == None or self.wolfR == self.sheep or self.wolfB == self.wolfR):
                self.wolfR = (random.randint(0,dim), random.randint(0,dim))
        self.grid[self.sheep[0]][self.sheep[1]] = State.SHEEP_R
        self.grid[self.wolfB[0]][self.wolfB[1]] = State.WOLFB_R
        self.grid[self.wolfR[0]][self.wolfR[1]] = State.WOLFR_R
        self.w_m_count = 0
        #self.reassign_wolves()
        
    def display(self):
        print(self.grid)

    def manhattan(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return abs(x1-x2) + abs(y1 - y2)

    def reassign_wolves(self):
        bLoc = (self.sheep[0] + 1, self.sheep[1])
        rLoc = (self.sheep[0], self.sheep[1] + 1)

        if not (self.manhattan(bLoc, self.wolfR) - self.manhattan(bLoc, self.wolfB) > 0):
            temp = (self.wolfR[0], self.wolfR[1])
            self.wolfR = (self.wolfB[0], self.wolfB[1])
            self.wolfB = temp
            

    def move(self):
        if self.turn == State.SHEEP:
            self.grid[self.sheep[0]][self.sheep[1]] = 0
            self.sheepMove()
            self.grid[self.sheep[0]][self.sheep[1]] = State.SHEEP_R
            self.turn = State.WOLF
        else:
            self.w_m_count += 1
            self.grid[self.wolfB[0]][self.wolfB[1]] = 0
            self.grid[self.wolfR[0]][self.wolfR[1]] = 0
            self.wolfMove()
            self.grid[self.wolfB[0]][self.wolfB[1]] = State.WOLFB_R
            self.grid[self.wolfR[0]][self.wolfR[1]] = State.WOLFR_R
            #self.checkStall()
            self.turn = State.SHEEP
        if self.grid[0][0] == State.SHEEP_R and self.grid[1][0] != 0 and self.grid[0][1] != 0:
            return False
        return True

    def checkStall(self):
        oldB = self.wolfB
        oldR = self.wolfR
        caught = False
        dim = self.dim - 1
        if self.grid[dim][0] == State.SHEEP_R and self.grid[dim][1] != 0 and self.grid[dim - 1][0] != 0:
            self.wolfB = (self.wolfB[0] - 1, self.wolfB[1])
        if self.grid[0][dim] == State.SHEEP_R and self.grid[1][dim] != 0 and self.grid[0][dim - 1] != 0:
            self.wolfR = (self.wolfB[0], self.wolfB[1] - 1)
        if self.grid[dim][dim] == State.SHEEP_R and self.grid[dim - 1][dim] != 0 and self.grid[dim][dim-1] != 0:
            self.wolfR = (self.wolfR[0], self.wolfR[1] - 1)
        self.grid[oldR[0]][oldR[1]] = 0
        self.grid[oldB[0]][oldB[1]] = 0
        #self.reassign_wolves()
        self.grid[self.wolfB[0]][self.wolfB[1]] = State.WOLFB_R
        self.grid[self.wolfR[0]][self.wolfR[1]] = State.WOLFR_R
        

    def sheepMove(self):
        temp = self.sheep
        self.sheep = random.choice(self.getSheepMovementOptions())
        if temp == self.sheep:
            return False
        return True

    def bounds(self, coord):
        x, y = coord
        if x < 0 or y < 0:
            return False
        if x >= self.dim or y >= self.dim:
            return False
        return True

    def getMoves(self):
        return self.w_m_count

    def getSheepMovementOptions(self):
        x, y = self.sheep
        locations = []
        candidates = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        for newLoc in candidates:
            if not (newLoc == self.wolfB or newLoc == self.wolfR) and self.bounds(newLoc):
                locations.append(newLoc)
        if len(locations) == 0:
            locations.append(self.sheep)
        return locations
    
    def wolfMove(self):
        oldB = self.wolfB
        oldR = self.wolfR
        self.moveWolfB()
        self.moveWolfR()
        #print(self.wolfB, self.wolfR)
        if self.wolfB == self.sheep or not self.bounds(self.wolfB):
            self.wolfB = oldB
        if self.wolfR == self.sheep or not self.bounds(self.wolfR):
            self.wolfR = oldR
        if self.wolfB == self.wolfR:
            if self.wolfB == oldR:
                self.wolfB = oldB#TODO: FIX THIS, LET OPTIMIZED THRU??
            else:
                self.wolfR = oldR
        if self.wolfB == self.wolfR:
            self.wolfB = (self.wolfB[0] - 1, self.wolfB[1])
        assert self.wolfB != self.wolfR
        assert self.wolfB != self.sheep 
        assert self.wolfR != self.sheep
    
    def moveWolfB(self):
        mS, nS = self.sheep
        mW, nW = self.wolfB
        if self.getMoves() < 2:
            #print(self.getMoves())
            pass
            self.wolfB = (mW, nW)
        elif not self.optimzedB():
            if mW > mS:
                if nW > nS:
                    self.wolfB = (mW, nW-1)
                else:
                    self.wolfB = (mW, nW + 1)
            else:
                self.wolfB = (mW+1, nW)
        else:
            if abs(nW - nS) == 1:
                self.wolfB = (mW, nS)
            else:
                self.wolfB = (mW-1, nW)

    def moveWolfR(self):
        mS, nS = self.sheep
        mW, nW = self.wolfR
        if self.getMoves() < 2:
            pass
        elif nW  > 5:
            self.wolfR = (mW, nW - 1)
        elif mS - mW > 4:
            self.wolfR = (mW + 1, nW)
        elif not self.optimzedR():
            if nW > nS:
                if mW > mS:
                    self.wolfR = (mW - 1, nW)
                else:
                    self.wolfR = (mW + 1, nW)
            else:
                self.wolfR = (mW, nW + 1)
        else:
            if abs(mW - mS) == 1:
                self.wolfR = (mS, nW)
            else:
                self.wolfR = (mW, nW - 1)

    def optimzedB(self):
        bM, bN = self.wolfB
        sM, sN = self.sheep
        if bM > sM and abs(bN - sN) <= 1:
            return True
        return False
    
    def optimzedR(self):
        rM, rN = self.wolfR
        sM, sN = self.sheep
        if rN > sN and abs(rM - sM) <= 1:
            return True
        return False



total_count = 0
runs = 10000
for _ in range(runs):
    x = State(8, (4,0), (6,3), (0,7))
    while x.move():
        #x.display()
        if total_count/runs > 100:
            x.display()
            time.sleep(1)
        #x.display()
        #time.sleep(1)
    total_count += x.getMoves()

print(total_count/runs)