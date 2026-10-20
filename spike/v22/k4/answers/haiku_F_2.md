### T01
```
n = 10
total = 0
for i in span(1, n):
    total = plus(total, i)
say(cat("sum=", str(total)))
```

### T02
```
aList = [10, 20, 30, 40]
x = at(aList, 3)
y = at(aList, len(aList))
cLine = cat("third=", str(x))
cLine = cat(cLine, " last=")
cLine = cat(cLine, str(y))
say(cLine)
```

### T03
```
aItems = ["1", "01", "1.0", "x", 2]
nCount = 0
for item in aItems:
    if eq(item, 1):
        nCount = plus(nCount, 1)
say(cat("count=", str(nCount)))
```

### T04
```
cName = "item"
n = 5
say(cat(cat(cName, "-"), str(n)))
```

### T05
```
n = 5
cLine = ""
for i in span(1, n):
    if gt(i, 1):
        cLine = cat(cLine, " ")
    cLine = cat(cLine, str(i))
say(cLine)
```

### T06
```
cText = "ring plus plus"
nVowels = 0
for i in span(1, len(cText)):
    ch = at(cText, i)
    if eq(ch, "a") or eq(ch, "e") or eq(ch, "i") or eq(ch, "o") or eq(ch, "u"):
        nVowels = plus(nVowels, 1)
say(cat("vowels=", str(nVowels)))
```

### T07
```
aList = [1, 2, 3, 4, 5]
cLine = ""
for i in span(len(aList), 1, -1):
    if len(cLine) > 0:
        cLine = cat(cLine, " ")
    cLine = cat(cLine, str(at(aList, i)))
say(cLine)
```

### T08
```
n = 6
fact = 1
for i in span(1, n):
    fact = fact * i
say(cat("fact=", str(fact)))
```

### T09
```
n = 10
cLine = ""
nA = 1
nB = 1
for i in span(1, n):
    if len(cLine) > 0:
        cLine = cat(cLine, " ")
    cLine = cat(cLine, str(nA))
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
    def Value(self):
        return self.nCount

o = new(Counter)
for i in span(1, nTimes):
    o.Add()
say(cat("count=", str(o.Value())))
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
xMax = at(aList, 1)
for i in span(1, len(aList)):
    if gt(at(aList, i), xMax):
        xMax = at(aList, i)
say(cat("max=", str(xMax)))
```

### T13
```
cText = "the quick brown fox"
nWords = 0
nInWord = 0
for i in span(1, len(cText)):
    ch = at(cText, i)
    if eq(ch, " "):
        nInWord = 0
    else:
        if nInWord == 0:
            nWords = plus(nWords, 1)
        nInWord = 1
say(cat("words=", str(nWords)))
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
nAge = 0
for i in span(1, len(aPeople)):
    person = at(aPeople, i)
    if eq(at(person, 1), cWho):
        nAge = at(person, 2)
say(cat("age=", str(nAge)))
```

### T15
```
n = 3
for i in span(1, n):
    cLine = ""
    for j in span(1, n):
        if gt(j, 1):
            cLine = cat(cLine, " ")
        cLine = cat(cLine, str(i * j))
    say(cLine)
```

### T16
```
a = 7
b = 2
q = floor(a / b)
r = mod(a, b)
cLine = cat("q=", str(q))
cLine = cat(cLine, " r=")
cLine = cat(cLine, str(r))
say(cLine)
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
if a > b and b != 5:
    say("out=1")
else:
    say("out=0")
```

### T19
```
aList = [1, 2, 2, 3, 3, 3]
nDistinct = 0
for i in span(1, len(aList)):
    nItem = at(aList, i)
    nSeen = 0
    for j in span(1, i):
        if lt(j, i) and eq(at(aList, j), nItem):
            nSeen = 1
    if nSeen == 0:
        nDistinct = plus(nDistinct, 1)
say(cat("distinct=", str(nDistinct)))
```

### T20
```
cDigits = "12345"
nSum = 0
for i in span(1, len(cDigits)):
    nSum = plus(nSum, plus(0, at(cDigits, i)))
say(cat("sum=", str(nSum)))
```
