### T01
```
n = 10
nSum = 0
for i = 1 to n
    nSum += i
next
see "sum=" + nSum + nl
```

### T02
```
aList = [10, 20, 30, 40]
see "third=" + aList[3] + " last=" + aList[len(aList)] + nl
```

### T03
```
aItems = ["1", "01", "1.0", "x", 2]
nCount = 0
for i = 1 to len(aItems)
    if aItems[i] = 1
        nCount++
    ok
next
see "count=" + nCount + nl
```

### T04
```
cName = "item"
n = 5
see cName + "-" + n + nl
```

### T05
```
n = 5
cOut = ""
for i = 1 to n
    if i > 1
        cOut += " "
    ok
    cOut += string(i)
next
see cOut + nl
```

### T06
```
cText = "ring plus plus"
aVowels = ["a", "e", "i", "o", "u"]
nVowels = 0
for i = 1 to len(cText)
    if find(aVowels, cText[i]) > 0
        nVowels++
    ok
next
see "vowels=" + nVowels + nl
```

### T07
```
aList = [1, 2, 3, 4, 5]
cOut = ""
for i = len(aList) to 1 step -1
    if i < len(aList)
        cOut += " "
    ok
    cOut += string(aList[i])
next
see cOut + nl
```

### T08
```
n = 6
nFact = 1
for i = 1 to n
    nFact *= i
next
see "fact=" + nFact + nl
```

### T09
```
n = 10
nA = 1
nB = 1
cOut = ""
for i = 1 to n
    if i > 1
        cOut += " "
    ok
    cOut += string(nA)
    nNext = nA + nB
    nA = nB
    nB = nNext
next
see cOut + nl
```

### T10
```
nTimes = 3
oCounter = new Counter
for i = 1 to nTimes
    oCounter.Add()
next
see "count=" + oCounter.Value() + nl

class Counter
    nCount = 0
    func Add
        nCount += 1
    func Value
        return nCount
```

### T11
```
cTag = "x"
try
    Missing()
catch
    see "caught-" + cTag + nl
done
see "done" + nl
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
see "max=" + nMax + nl
```

### T13
```
cText = "the quick brown fox"
nWords = 0
bIn = 0
for i = 1 to len(cText)
    if cText[i] != " "
        if bIn = 0
            nWords++
            bIn = 1
        ok
    else
        bIn = 0
    ok
next
see "words=" + nWords + nl
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
see "age=" + nAge + nl
```

### T15
```
n = 3
for i = 1 to n
    cRow = ""
    for j = 1 to n
        if j > 1
            cRow += " "
        ok
        cRow += string(i * j)
    next
    see cRow + nl
next
```

### T16
```
a = 7
b = 2
q = floor(a / b)
r = a - b * q
see "q=" + q + " r=" + r + nl
```

### T17
```
cPiece = "ab"
n = 3
cOut = ""
for i = 1 to n
    cOut += cPiece
next
see cOut + nl
```

### T18
```
a = 3
b = 2
if a > b and b != 5
    see "out=1" + nl
else
    see "out=0" + nl
ok
```

### T19
```
aList = [1, 2, 2, 3, 3, 3]
aSeen = []
for i = 1 to len(aList)
    if find(aSeen, aList[i]) = 0
        add(aSeen, aList[i])
    ok
next
see "distinct=" + len(aSeen) + nl
```

### T20
```
cDigits = "12345"
nSum = 0
for i = 1 to len(cDigits)
    nSum += number(cDigits[i])
next
see "sum=" + nSum + nl
```
