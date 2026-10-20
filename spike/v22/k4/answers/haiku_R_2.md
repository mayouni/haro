### T01
```
n = 10
nSum = 0
for i = 1 to n
    nSum = nSum + i
next
? "sum=" + nSum
```

### T02
```
aList = [10, 20, 30, 40]
? "third=" + aList[3] + " last=" + aList[len(aList)]
```

### T03
```
aItems = ["1", "01", "1.0", "x", 2]
nCount = 0
for i = 1 to len(aItems)
    if aItems[i] = 1
        nCount = nCount + 1
    ok
next
? "count=" + nCount
```

### T04
```
cName = "item"
n = 5
? cName + "-" + n
```

### T05
```
n = 5
cLine = ""
for i = 1 to n
    if i > 1
        cLine = cLine + " "
    ok
    cLine = cLine + i
next
? cLine
```

### T06
```
cText = "ring plus plus"
nVowels = 0
for i = 1 to len(cText)
    cChar = cText[i]
    if cChar = "a" or cChar = "e" or cChar = "i" or cChar = "o" or cChar = "u"
        nVowels = nVowels + 1
    ok
next
? "vowels=" + nVowels
```

### T07
```
aList = [1, 2, 3, 4, 5]
cOut = ""
for i = len(aList) to 1 step -1
    cOut = cOut + aList[i]
    if i > 1
        cOut = cOut + " "
    ok
next
? cOut
```

### T08
```
n = 6
nFact = 1
for i = 2 to n
    nFact = nFact * i
next
? "fact=" + nFact
```

### T09
```
n = 10
cOut = ""
nA = 1
nB = 1
for i = 1 to n
    if i > 1
        cOut = cOut + " "
    ok
    cOut = cOut + nA
    nT = nA + nB
    nA = nB
    nB = nT
next
? cOut
```

### T10
```
nTimes = 3
oCounter = new Counter
for i = 1 to nTimes
    oCounter.Add()
next
? "count=" + oCounter.Value()

class Counter
    nCount = 0
    func Add()
        This.nCount = This.nCount + 1
    func Value()
        return This.nCount
```

### T11
```
cTag = "x"
try
    Missing()
catch
    ? "caught-" + cTag
done
? "done"
```

### T12
```
aList = [3, 9, 2, 7]
nMax = aList[1]
for i = 1 to len(aList)
    if aList[i] > nMax
        nMax = aList[i]
    ok
next
? "max=" + nMax
```

### T13
```
cText = "the quick brown fox"
nWords = 0
nIn = 0
for i = 1 to len(cText)
    if cText[i] = " "
        nIn = 0
    else
        if nIn = 0
            nWords = nWords + 1
            nIn = 1
        ok
    ok
next
? "words=" + nWords
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
nAge = 0
for i = 1 to len(aPeople)
    if aPeople[i][1] = cWho
        nAge = aPeople[i][2]
    ok
next
? "age=" + nAge
```

### T15
```
n = 3
for i = 1 to n
    cRow = ""
    for j = 1 to n
        if j > 1
            cRow = cRow + " "
        ok
        cRow = cRow + (i * j)
    next
    ? cRow
next
```

### T16
```
a = 7
b = 2
nQ = floor(a / b)
nR = a % b
? "q=" + nQ + " r=" + nR
```

### T17
```
cPiece = "ab"
n = 3
cOut = ""
for i = 1 to n
    cOut = cOut + cPiece
next
? cOut
```

### T18
```
a = 3
b = 2
if a > b and b != 5
    ? "out=1"
else
    ? "out=0"
ok
```

### T19
```
aList = [1, 2, 2, 3, 3, 3]
aSeen = []
for i = 1 to len(aList)
    nFound = 0
    for j = 1 to len(aSeen)
        if aSeen[j] = aList[i]
            nFound = 1
        ok
    next
    if nFound = 0
        add(aSeen, aList[i])
    ok
next
? "distinct=" + len(aSeen)
```

### T20
```
cDigits = "12345"
nSum = 0
for i = 1 to len(cDigits)
    nSum = nSum + number(cDigits[i])
next
? "sum=" + nSum
```
