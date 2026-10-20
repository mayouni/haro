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
line = cat("third=", at(aList, 3))
line = cat(line, " last=")
line = cat(line, at(aList, len(aList)))
say(line)
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
vowels = 0
for i in span(1, len(cText)):
    ch = at(cText, i)
    if eq(ch, "a") or eq(ch, "e") or eq(ch, "i") or eq(ch, "o") or eq(ch, "u"):
        vowels = plus(vowels, 1)
say(cat("vowels=", vowels))
```

### T07
```
aList = [1, 2, 3, 4, 5]
n = len(aList)
line = cat("", at(aList, n))
for i in span(n - 1, 1, -1):
    line = cat(cat(line, " "), at(aList, i))
say(line)
```

### T08
```
n = 6
f = 1
for i in span(1, n):
    f = f * i
say(cat("fact=", f))
```

### T09
```
n = 10
line = ""
a = 1
b = 1
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
c = new(Counter)
for i in span(1, nTimes):
    c.Add()
say(cat("count=", c.Value()))

class Counter:
    def __region__(self):
        self.n = 0
    def Add(self):
        self.n = plus(self.n, 1)
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
words = 0
inWord = 0
for i in span(1, len(cText)):
    ch = at(cText, i)
    if eq(ch, " "):
        inWord = 0
    else:
        if eq(inWord, 0):
            words = plus(words, 1)
        inWord = 1
say(cat("words=", words))
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
age = 0
for p in aPeople:
    if eq(at(p, 1), cWho):
        age = at(p, 2)
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
line = cat("q=", q)
line = cat(line, " r=")
line = cat(line, r)
say(line)
```

### T17
```
cPiece = "ab"
n = 3
out = ""
for i in span(1, n):
    out = cat(out, cPiece)
say(out)
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
n = len(aList)
distinct = 0
for i in span(1, n):
    x = at(aList, i)
    first = 1
    for j in span(1, n):
        if lt(j, i) and eq(at(aList, j), x):
            first = 0
    if eq(first, 1):
        distinct = plus(distinct, 1)
say(cat("distinct=", distinct))
```

### T20
```
cDigits = "12345"
total = 0
for i in span(1, len(cDigits)):
    total = plus(total, at(cDigits, i))
say(cat("sum=", total))
```
