### T01
```
n = 10
nSum = 0
for i in span(1, n):
    nSum = plus(nSum, i)
say(cat("sum=", nSum))
```

### T02
```
aList = [10, 20, 30, 40]
xThird = at(aList, 3)
yLast = at(aList, len(aList))
cOut = cat("third=", xThird)
cOut = cat(cOut, " last=")
cOut = cat(cOut, yLast)
say(cOut)
```

### T03
```
aItems = ["1", "01", "1.0", "x", 2]
nCount = 0
for x in aItems:
    if eq(x, 1):
        nCount = plus(nCount, 1)
say(cat("count=", nCount))
```

### T04
```
cName = "item"
n = 5
cOut = cat(cName, "-")
cOut = cat(cOut, n)
say(cOut)
```

### T05
```
n = 5
cLine = ""
for i in span(1, n):
    if eq(i, 1):
        cLine = cat(cLine, i)
    else:
        cLine = cat(cLine, " ")
        cLine = cat(cLine, i)
say(cLine)
```

### T06
```
cText = "ring plus plus"
nVowels = 0
for i in span(1, len(cText)):
    c = at(cText, i)
    if eq(c, "a") or eq(c, "e") or eq(c, "i") or eq(c, "o") or eq(c, "u"):
        nVowels = plus(nVowels, 1)
say(cat("vowels=", nVowels))
```

### T07
```
aList = [1, 2, 3, 4, 5]
cLine = ""
for i in span(len(aList), 1, -1):
    if ne(i, len(aList)):
        cLine = cat(cLine, " ")
    cLine = cat(cLine, at(aList, i))
say(cLine)
```

### T08
```
n = 6
nFact = 1
for i in span(1, n):
    nFact = nFact * i
say(cat("fact=", nFact))
```

### T09
```
n = 10
nA = 1
nB = 1
cLine = ""
for i in span(1, n):
    if eq(i, 1):
        cLine = cat(cLine, nA)
    else:
        cLine = cat(cLine, " ")
        cLine = cat(cLine, nA)
    nT = plus(nA, nB)
    nA = nB
    nB = nT
say(cLine)
```

### T10
```
nTimes = 3
oC = new(Counter)
for i in span(1, nTimes):
    oC.Add()
say(cat("count=", oC.Value()))

class Counter:
    def __region__(self):
        self.nCount = 0
    def Add(self):
        self.nCount = plus(self.nCount, 1)
        return ""
    def Value(self):
        return self.nCount
```

### T11
```
cTag = "x"
try:
    Missing()
except RingError as e:
    say(cat("caught-", cTag))
say("done")
```

### T12
```
aList = [3, 9, 2, 7]
nMax = at(aList, 1)
for x in aList:
    if gt(x, nMax):
        nMax = x
say(cat("max=", nMax))
```

### T13
```
cText = "the quick brown fox"
nWords = 0
nIn = 0
for i in span(1, len(cText)):
    c = at(cText, i)
    if eq(c, " "):
        nIn = 0
    else:
        if eq(nIn, 0):
            nWords = plus(nWords, 1)
        nIn = 1
say(cat("words=", nWords))
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
nAge = ""
for p in aPeople:
    if eq(at(p, 1), cWho):
        nAge = at(p, 2)
say(cat("age=", nAge))
```

### T15
```
n = 3
for i in span(1, n):
    cLine = ""
    for j in span(1, n):
        nProd = i * j
        if eq(j, 1):
            cLine = cat(cLine, nProd)
        else:
            cLine = cat(cLine, " ")
            cLine = cat(cLine, nProd)
    say(cLine)
```

### T16
```
a = 7
b = 2
nQ = floor(a / b)
nR = mod(a, b)
cOut = cat("q=", nQ)
cOut = cat(cOut, " r=")
cOut = cat(cOut, nR)
say(cOut)
```

### T17
```
cPiece = "ab"
n = 3
cOut = ""
for i in span(1, n):
    cOut = cat(cOut, cPiece)
say(cOut)
```

### T18
```
a = 3
b = 2
if gt(a, b) and ne(b, 5):
    say("out=1")
else:
    say("out=0")
```

### T19
```
aList = [1, 2, 2, 3, 3, 3]
nDistinct = 0
for i in span(1, len(aList)):
    nDup = 0
    for j in span(1, len(aList)):
        if lt(j, i) and eq(at(aList, j), at(aList, i)):
            nDup = 1
    if eq(nDup, 0):
        nDistinct = plus(nDistinct, 1)
say(cat("distinct=", nDistinct))
```

### T20
```
cDigits = "12345"
nSum = 0
for i in span(1, len(cDigits)):
    nSum = plus(nSum, at(cDigits, i))
say(cat("sum=", nSum))
```
