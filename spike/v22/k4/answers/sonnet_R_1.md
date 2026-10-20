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
    try
        if aItems[i] = 1
            nCount = nCount + 1
        ok
    catch
        nCount = nCount + 0
    done
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
cOut = ""
for i = 1 to n
    if i > 1
        cOut = cOut + " "
    ok
    cOut = cOut + i
next
? cOut
```

### T06
```
cText = "ring plus plus"
nVowels = 0
for i = 1 to len(cText)
    c = cText[i]
    if c = "a" or c = "e" or c = "i" or c = "o" or c = "u"
        nVowels = nVowels + 1
    ok
next
? "vowels=" + nVowels
```

### T07
```
aList = [1, 2, 3, 4, 5]
nLen = len(aList)
cOut = ""
for i = 1 to nLen
    if i > 1
        cOut = cOut + " "
    ok
    cOut = cOut + aList[nLen - i + 1]
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
nA = 1
nB = 1
cOut = ""
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
o = new Counter
for i = 1 to nTimes
    o.Add()
next
nResult = o.Value()
? "count=" + nResult

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
for i = 2 to len(aList)
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
bIn = 0
for i = 1 to len(cText)
    c = cText[i]
    if c = " "
        bIn = 0
    else
        if bIn = 0
            nWords = nWords + 1
            bIn = 1
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
        exit
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
nDistinct = 0
for i = 1 to len(aList)
    bNew = 1
    for j = 1 to i - 1
        if aList[j] = aList[i]
            bNew = 0
        ok
    next
    if bNew = 1
        nDistinct = nDistinct + 1
    ok
next
? "distinct=" + nDistinct
```

### T20
```
cDigits = "12345"
nSum = 0
for i = 1 to len(cDigits)
    c = cDigits[i]
    if c >= "0" and c <= "9"
        nSum = nSum + number(c)
    ok
next
? "sum=" + nSum
```
