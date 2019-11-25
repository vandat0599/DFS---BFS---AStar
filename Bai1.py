import copy
import operator

class Literal():
    def __init__(self, liter):
        self.char = liter[1] if '-' in liter else liter[0]
        self.isNeg = '-' in liter
    
    def __eq__(self, value):
        return self.char == value.char and self.isNeg == value.isNeg
    
    def __hash__(self):
        return hash(('char', self.char,
                 'isNeg', self.isNeg))
    
    def __lt__(self, value):
        return self.char < value.char

    def getNegative(self):
        l = copy.deepcopy(self)
        l.char = self.char
        l.isNeg = not(self.isNeg)
        return l
    
    def __str__(self):
        return self.char if self.isNeg==False else "-{}".format(self.char)


class Clause:
    def __init__(self, liters):
        self.liters = [Literal(l) for l in [ l.strip() for l in liters.split("OR")]]

    def __eq__(self, value):
        opSelf = self.getOptimize()
        opValue = value.getOptimize()
        if(len(opSelf.liters)==len(opValue.liters)):
            for l in opValue.liters:
                if l not in opSelf.liters:
                    return False
            return True
        return False

    def __str__(self):
        opClause = self.getOptimize()
        if opClause.liters:
            result = ""
            for i in range(0,len(opClause.liters) - 1):
                result += str(opClause.liters[i]) + " OR "
            result += str(opClause.liters[len(opClause.liters)-1])
            return result
        return "{}"

    def __add__(self, value):
        result = copy.deepcopy(self)
        result.liters += value.liters
        return result

    def getNegative(self):
        res = list()
        for l in self.liters:
          res.append(l.getNegative())
        return res
    
    def getOptimize(self):
        result = copy.deepcopy(self)
        for l in result.liters:
            if l.getNegative() in result.liters:
                result.liters.remove(l)
                result.liters.remove(l.getNegative())
        result.liters = list(set(result.liters))
        result.liters.sort()
        return result
    
    def isTrueClause(self):
        for l in self.liters:
            if l.getNegative() in self.liters:
                return True
        False

def PLResolve(c1,c2):
    result = list()
    for i in range(len(c2.liters)):
        c1Ins = copy.deepcopy(c1)
        c2Ins = copy.deepcopy(c2)
        if c2.liters[i].getNegative() in c1.liters:
            c1Ins.liters.remove(c2.liters[i].getNegative())
            c2Ins.liters.remove(c2.liters[i])
            res = c1Ins + c2Ins
            if res not in result:
                result.append(res)
    return result

def  PLResolution(kb,a,fOut):
    clauses = copy.deepcopy(kb)
    for literal in a.getNegative():
        clauses.append(Clause(str(literal)))
    new = list()
    while(True):
        clauseGenerate = list()
        for i in range(len(clauses)-1):
            for j in range(i + 1, len(clauses)):
                resolvents = PLResolve(clauses[i],clauses[j])
                for re in resolvents:
                    if not(re.isTrueClause()) and\
                            re.getOptimize() not in new and\
                            re.getOptimize() not in clauseGenerate and\
                            re.getOptimize() not in clauses:
                        clauseGenerate.append(re.getOptimize())
        #write file here
        fOut.write(str(len(clauseGenerate))+'\n')
        # print(len(clauseGenerate))
        for i in clauseGenerate:
            fOut.write(str(i)+'\n')
            # print(str(i))
        for i in clauseGenerate:
            if str(i)=="{}":
                fOut.write("YES\n")
                return True
        new += clauseGenerate
        if all(elem in clauses  for elem in new):
            fOut.write("NO\n")
            return False
        for n in new:
            if n not in clauses:
                clauses.append(n)
    return False

def main():
    #<data handler>
    a = ""
    kb = list()
    with open("input_1.txt") as f:
        lineList = f.readlines()
    a = Clause(lineList[0].strip())
    for i in range(int(lineList[1])):
        kb.append(Clause(lineList[i+2].strip()))
    #<data handler/>
    fOut = open("output.txt", "w")
    PLResolution(kb,a,fOut)
main()