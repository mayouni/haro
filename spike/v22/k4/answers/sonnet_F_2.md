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
count = 0
for x in aItems:
    if eq(x, 1):
        count = plus(count, 1)
say(cat("count=", count))
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
line = ""
for i in span(1, n):
    if eq(i, 1):
        line = cat(line, i)
    else:
        line = cat(cat(line, " "), i)
say(line)
```

### T06
```
cText = "ring plus plus"
count = 0
for i in span(1, len(cText)):
    c = at(cText, i)
    if eq(c, "a") or eq(c, "e") or eq(c, "i") or eq(c, "o") or eq(c, "u"):
        count = plus(count, 1)
say(cat("vowels=", count))
```

### T07
```
aList = [1, 2, 3, 4, 5]
line = ""
isFirst = 1
for i in span(len(aList), 1, -1):
    if eq(isFirst, 1):
        line = cat(line, at(aList, i))
    else:
        line = cat(cat(line, " "), at(aList, i))
    isFirst = 0
say(line)
```

### T08
```
n = 6
result = 1
for i in span(1, n):
    result = result * i
say(cat("fact=", result))
```

### T09
```
n = 10
a = 1
b = 1
line = ""
for i in span(1, n):
    if eq(i, 1):
        line = cat(line, a)
    else:
        line = cat(cat(line, " "), a)
    t = plus(a, b)
    a = b
    b = t
say(line)
```

### T10
```
nTimes = 3
class Counter:
    def __region__(self):
        self.n = 0
    def Add(self):
        self.n = plus(self.n, 1)
        return ""
    def Value(self):
        return self.n
o = new(Counter)
for i in span(1, nTimes):
    o.Add()
say(cat("count=", o.Value()))
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
m = at(aList, 1)
for x in aList:
    if gt(x, m):
        m = x
say(cat("max=", m))
```

### T13
```
cText = "the quick brown fox"
inWord = 0
count = 0
for i in span(1, len(cText)):
    c = at(cText, i)
    if eq(c, " "):
        inWord = 0
    else:
        if eq(inWord, 0):
            count = plus(count, 1)
        inWord = 1
say(cat("words=", count))
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
age = ""
found = 0
for p in aPeople:
    if eq(found, 0) and eq(at(p, 1), cWho):
        age = at(p, 2)
        found = 1
say(cat("age=", age))
```

### T15
```
n = 3
for i in span(1, n):
    line = ""
    for j in span(1, n):
        if eq(j, 1):
            line = cat(line, i * j)
        else:
            line = cat(cat(line, " "), i * j)
    say(line)
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
s = ""
for i in span(1, n):
    s = cat(s, cPiece)
say(s)
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
count = 0
for i in span(1, len(aList)):
    isNew = 1
    for j in span(1, len(aList)):
        if lt(j, i) and eq(at(aList, j), at(aList, i)):
            isNew = 0
    if eq(isNew, 1):
        count = plus(count, 1)
say(cat("distinct=", count))
```

### T20
```
cDigits = "12345"
total = 0
for i in span(1, len(cDigits)):
    d = at(cDigits, i)
    total = plus(total, d)
say(cat("sum=", total))
```
