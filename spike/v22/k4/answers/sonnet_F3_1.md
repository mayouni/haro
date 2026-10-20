### T01
```
n = 10
total = 0
for i in span(1, n):
    total = plus(total, i)
say(cat("sum=", total))
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
cOut = ""
for i in span(1, n):
    if gt(i, 1):
        cOut = cat(cOut, " ")
    cOut = cat(cOut, i)
say(cOut)
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
cOut = ""
for i in span(len(aList), 1, -1):
    if lt(i, len(aList)):
        cOut = cat(cOut, " ")
    cOut = cat(cOut, at(aList, i))
say(cOut)
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
a = 1
b = 1
cOut = ""
for i in span(1, n):
    if gt(i, 1):
        cOut = cat(cOut, " ")
    cOut = cat(cOut, a)
    t = plus(a, b)
    a = b
    b = t
say(cOut)
```

### T10
```
nTimes = 3
o = new_without_init(Counter)
for i in span(1, nTimes):
    o.Add()
say(cat("count=", o.Value()))

class Counter:
    def __region__(self):
        self.n = 0
    def Add(self):
        self.n = plus(self.n, 1)
        return ""
    def Value(self):
        return self.n
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
best = at(aList, 1)
for x in aList:
    if gt(x, best):
        best = x
say(cat("max=", best))
```

### T13
```
cText = "the quick brown fox"
nWords = 0
inWord = 0
for i in span(1, len(cText)):
    c = at(cText, i)
    if eq(c, " "):
        inWord = 0
    else:
        if eq(inWord, 0):
            nWords = plus(nWords, 1)
        inWord = 1
say(cat("words=", nWords))
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
age = ""
for p in aPeople:
    if eq(at(p, 1), cWho):
        age = at(p, 2)
say(cat("age=", age))
```

### T15
```
n = 3
for i in span(1, n):
    cOut = ""
    for j in span(1, n):
        if gt(j, 1):
            cOut = cat(cOut, " ")
        cOut = cat(cOut, i * j)
    say(cOut)
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
    isNew = 1
    for j in span(1, len(aList)):
        if lt(j, i) and eq(at(aList, j), at(aList, i)):
            isNew = 0
    if eq(isNew, 1):
        nDistinct = plus(nDistinct, 1)
say(cat("distinct=", nDistinct))
```

### T20
```
cDigits = "12345"
total = 0
for i in span(1, len(cDigits)):
    total = plus(total, at(cDigits, i))
say(cat("sum=", total))
```
