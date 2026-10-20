### T01
```
n = 10
nSum = 0
nI = 1
while nI <= n
    nSum += nI
    nI += 1
end
? "sum=" + string(nSum)
```

### T02
```
aList = [10, 20, 30, 40]
? "third=" + string(aList[3]) + " last=" + string(aList[len(aList)])
```

### T03
```
aItems = ["1", "01", "1.0", "x", 2]
nCount = 0
nI = 1
while nI <= len(aItems)
    if aItems[nI] = 1
        nCount += 1
    ok
    nI += 1
end
? "count=" + string(nCount)
```

### T04
```
cName = "item"
n = 5
? cName + "-" + string(n)
```

### T05
```
n = 5
cOut = ""
nI = 1
while nI <= n
    if nI > 1
        cOut += " "
    ok
    cOut += string(nI)
    nI += 1
end
? cOut
```

### T06
```
cText = "ring plus plus"
nVowels = 0
nI = 1
while nI <= len(cText)
    cChar = substr(cText, nI, 1)
    if cChar = "a" or cChar = "e" or cChar = "i" or cChar = "o" or cChar = "u"
        nVowels += 1
    ok
    nI += 1
end
? "vowels=" + string(nVowels)
```

### T07
```
aList = [1, 2, 3, 4, 5]
cOut = ""
nI = len(aList)
while nI >= 1
    if nI < len(aList)
        cOut += " "
    ok
    cOut += string(aList[nI])
    nI -= 1
end
? cOut
```

### T08
```
n = 6
nFact = 1
nI = 2
while nI <= n
    nFact *= nI
    nI += 1
end
? "fact=" + string(nFact)
```

### T09
```
n = 10
cOut = ""
nA = 1
nB = 1
nI = 1
while nI <= n
    if nI > 1
        cOut += " "
    ok
    cOut += string(nA)
    nT = nA + nB
    nA = nB
    nB = nT
    nI += 1
end
? cOut
```

### T10
```
nTimes = 3
o = new Counter
nI = 1
while nI <= nTimes
    o.Add()
    nI += 1
end
? "count=" + string(o.Value())

class Counter
    count = 0
    func Add()
        @count = @count + 1
    func Value()
        return @count
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
nI = 2
while nI <= len(aList)
    if aList[nI] > nMax
        nMax = aList[nI]
    ok
    nI += 1
end
? "max=" + string(nMax)
```

### T13
```
cText = "the quick brown fox"
nWords = 0
nInWord = 0
nI = 1
while nI <= len(cText)
    cChar = substr(cText, nI, 1)
    if cChar = " "
        nInWord = 0
    else
        if nInWord = 0
            nWords += 1
            nInWord = 1
        ok
    ok
    nI += 1
end
? "words=" + string(nWords)
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
nAge = 0
nI = 1
while nI <= len(aPeople)
    if aPeople[nI][1] = cWho
        nAge = aPeople[nI][2]
    ok
    nI += 1
end
? "age=" + string(nAge)
```

### T15
```
n = 3
nRow = 1
while nRow <= n
    cLine = ""
    nCol = 1
    while nCol <= n
        if nCol > 1
            cLine += " "
        ok
        cLine += string(nRow * nCol)
        nCol += 1
    end
    ? cLine
    nRow += 1
end
```

### T16
```
a = 7
b = 2
nQ = 0
nR = a
while nR < 0
    nR += b
    nQ -= 1
end
while nR >= b
    nR -= b
    nQ += 1
end
? "q=" + string(nQ) + " r=" + string(nR)
```

### T17
```
cPiece = "ab"
n = 3
cOut = ""
nI = 1
while nI <= n
    cOut += cPiece
    nI += 1
end
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
nI = 1
while nI <= len(aList)
    bDup = false
    nJ = 1
    while nJ < nI
        if aList[nJ] = aList[nI]
            bDup = true
        ok
        nJ += 1
    end
    if bDup = false
        nDistinct += 1
    ok
    nI += 1
end
? "distinct=" + string(nDistinct)
```

### T20
```
cDigits = "12345"
nSum = 0
nI = 1
while nI <= len(cDigits)
    nSum += number(substr(cDigits, nI, 1))
    nI += 1
end
? "sum=" + string(nSum)
```
