class Literal():
    def __init__(self, liter):
        self.char = liter[1] if '-' in liter else liter[0]
        self.isNeg = '-' in liter
    
    def __eq__(self, value):
        return self.char == value.char and self.isNeg == value.isNeg

    def getNegative(self):
        l = self
        l.char = self.char
        l.isNeg = not(self.isNeg)
        return l
    
    def __str__(self):
        return self.char if self.isNeg==False else "-{}".format(self.char)


class Clause:
    def __init__(self, liters):
        self.liters = [Literal(l) for l in [ l.strip() for l in liters.split("OR")]]

    def __eq__(self, value):
        for i in range(0,len(value.liters)):
            if self.liters[i]!=value.liters[i]:
                return False
        return True

    def __str__(self):
        result = ""
        for i in range(0,len(self.liters) - 1):
            result += str(self.liters[i]) + " OR "
        result += str(self.liters[len(self.liters)-1])
        return result

    def getNegative(self):
        res = list()
        for l in self.liters:
          res.append(l.getNegative())
        return res

def main():
    a = ""
    kb = list()
    with open("Input.txt") as f:
        lineList = f.readlines()
    a = lineList[0].strip()
    for i in range(int(lineList[1])):
        kb.append(Clause(lineList[i+2].strip()))
    
    
main()