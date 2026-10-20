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
say(cat(cat(cat("third=", at(aList, 3)), " last="), at(aList, len(aList))))
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
say(cat(cat(cName, "-"), n))
```

### T05
```
n = 5
cLine = ""
for i in span(1, n):
    if gt(i, 1):
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
    if lt(i, len(aList)):
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
    if gt(i, 1):
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
class Counter:
    def __region__(self):
        self.nCount = 0
    def Add(self):
        self.nCount = plus(self.nCount, 1)
        return ""
    def Value(self):
        return self.nCount
oC = new(Counter)
for i in span(1, nTimes):
    oC.Add()
say(cat("count=", oC.Value()))
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
nAge = 0
nFound = 0
for aPair in aPeople:
    if eq(nFound, 0) and eq(at(aPair, 1), cWho):
        nAge = at(aPair, 2)
        nFound = 1
say(cat("age=", nAge))
```

### T15
```
n = 3
for i in span(1, n):
    cRow = ""
    for j in span(1, n):
        if gt(j, 1):
            cRow = cat(cRow, " ")
        cRow = cat(cRow, i * j)
    say(cRow)
```

### T16
```
a = 7
b = 2
q = floor(a / b)
r = mod(a, b)
say(cat(cat(cat("q=", q), " r="), r))
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
