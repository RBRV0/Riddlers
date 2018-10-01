import numpy as np

template_1 = {0 : 0, 1 : 1, 2 : 0, 3 : 0, 4 : 8, 5 : 1, 6 : 1, 7 : 0, 8 : 1, 9 : 0, 10 : 0, 11 : 1, 12 : 1, 13 : 0, 14 : 1}


class Set:
    def __init__(self, template):
        self.balls = self.generate()
        self.template = template
        self.movements = 0
        self.wrongStripedKeys = None
        self.wrongSolidKeys = None
        self.eight = self.findEight()

    def generate(self):
        balls = np.array([0 for i in range(7)] + [1 for i in range(7)] + [8])
        return np.random.permutation(balls)

    def findEight(self):
        for index, i in enumerate(self.balls):
            if i == 8:
                return index

    def set(self, values):
        self.balls = np.array(values)

    def is_valid(self):
        valid = True
        for i in range(15):
            if self.balls[i] != self.template[i]:
                valid = False
        return valid

    def leftRotation(self):
        vect = self.balls
        self.balls = np.array([vect[10],
                               vect[11], vect[6],
                               vect[12], vect[7], vect[3],
                               vect[13], vect[8], vect[4], vect[1],
                               vect[14], vect[9], vect[5], vect[2], vect[0]])
        self.rightPosition = self.howWell()

    def leftRotationEvaluation(self):
        vect = self.balls
        hyp = Set(template_1)
        hyp.set(np.array([vect[10],
                               vect[11], vect[6],
                               vect[12], vect[7], vect[3],
                               vect[13], vect[8], vect[4], vect[1],
                               vect[14], vect[9], vect[5], vect[2], vect[0]]))
        return hyp.howWell()

    def rightRotation(self):
        self.leftRotation()
        self.leftRotation()

    def rightRotationEvaluation(self):
        vect = self.balls
        hyp = Set(template_1)
        hyp.set(np.array([vect[10],
                               vect[11], vect[6],
                               vect[12], vect[7], vect[3],
                               vect[13], vect[8], vect[4], vect[1],
                               vect[14], vect[9], vect[5], vect[2], vect[0]]))
        vect = hyp.balls
        hyp = Set(template_1)
        hyp.set(np.array([vect[10],
                               vect[11], vect[6],
                               vect[12], vect[7], vect[3],
                               vect[13], vect[8], vect[4], vect[1],
                               vect[14], vect[9], vect[5], vect[2], vect[0]]))
        return hyp.howWell()

    def switch(self, x, y):
        if self.balls[x] != self.balls[y]:
            self.movements += 1
        a = self.balls[x]
        b = self.balls[y]
        self.balls[x] = b
        self.balls[y] = a


    def howWell(self):
        result = 0
        for index, ball in enumerate(self.balls):
            if ball == template_1[index]:
                result += 1
        return result

    def wrongPositions(self):
        wrongStrips = []
        wrongSolids = []
        for index, ball in enumerate(self.balls):
            if ball != self.template[index]:
                if ball == 0:
                    wrongSolids.append(index)
                else:
                    wrongStrips.append(index)
        self.wrongSolidKeys = wrongSolids
        self.wrongStripedKeys = wrongStrips

    def solve(self):
        self.wrongPositions()
        while not self.is_valid():
            if self.leftRotationEvaluation() > self.howWell() + 2 or self.rightRotationEvaluation() > self.howWell() + 2:
                if self.leftRotationEvaluation() >= self.rightRotationEvaluation():
                    self.leftRotation()
                    self.movements += 1
                    self.wrongPositions()
                    self.eight = self.findEight()
                else:
                    self.rightRotation()
                    self.movements += 1
                    self.wrongPositions()
                    self.eight = self.findEight()
            elif self.eight != 4: # ball eight has the position no 4 in the template
                self.switch(self.eight, 4)
                self.eight = self.findEight()
                self.wrongPositions()
            elif len(self.wrongSolidKeys) != 0:# self.wrongSolidKeys is always as long as self.wrongStripedKeys
                self.switch(self.wrongStripedKeys[0], self.wrongSolidKeys[0])
                self.wrongPositions()

result = []
n = 100000
for i in range(n):
    louis = Set(template_1)
    louis.solve()
    result.append(louis.movements)

print("With {0} tries, the maximum of moves is {1}".format(n, max(result)))