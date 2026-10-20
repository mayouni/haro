### T01
```
n = 10
total = 0
i = 1
while le(i, n):
    total = plus(total, i)
    i = plus(i, 1)
say(cat("sum=", total))
```

### T02
```
aList = [10, 20, 30, 40]
third = at(aList, 3)
lastItem = at(aList, len(aList))
say(cat(cat(cat("third=", third), " last="), lastItem))
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
i = 1
while le(i, n):
    if eq(i, 1):
        line = cat(line, i)
    else:
        line = cat(cat(line, " "), i)
    i = plus(i, 1)
say(line)
```

### T06
```
cText = "ring plus plus"
vowels = 0
i = 1
while le(i, len(cText)):
    ch = at(cText, i)
    if eq(ch, "a") or eq(ch, "e") or eq(ch, "i") or eq(ch, "o") or eq(ch, "u"):
        vowels = plus(vowels, 1)
    i = plus(i, 1)
say(cat("vowels=", vowels))
```

### T07
```
aList = [1, 2, 3, 4, 5]
line = ""
for i in span(len(aList), 1, -1):
    if lt(i, len(aList)):
        line = cat(line, " ")
    line = cat(line, at(aList, i))
say(line)
```

### T08
```
n = 6
fact = 1
i = 1
while le(i, n):
    fact = fact * i
    i = plus(i, 1)
say(cat("fact=", fact))
```

### T09
```
n = 10
line = ""
a = 1
b = 1
i = 1
while le(i, n):
    if gt(i, 1):
        line = cat(line, " ")
    line = cat(line, a)
    nxt = plus(a, b)
    a = b
    b = nxt
    i = plus(i, 1)
say(line)
```

### T10
```
nTimes = 3
c = new(Counter)
i = 1
while le(i, nTimes):
    c.Add()
    i = plus(i, 1)
say(cat("count=", c.Value()))

class Counter:
    def __region__(self):
        self.count = 0
    def Add(self):
        self.count = plus(self.count, 1)
    def Value(self):
        return self.count
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
i = 1
while le(i, len(cText)):
    ch = at(cText, i)
    if eq(ch, " "):
        inWord = 0
    else:
        if eq(inWord, 0):
            words = plus(words, 1)
        inWord = 1
    i = plus(i, 1)
say(cat("words=", words))
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
age = 0
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
i = 1
while le(i, n):
    line = ""
    j = 1
    while le(j, n):
        if gt(j, 1):
            line = cat(line, " ")
        line = cat(line, i * j)
        j = plus(j, 1)
    say(line)
    i = plus(i, 1)
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
out = ""
i = 1
while le(i, n):
    out = cat(out, cPiece)
    i = plus(i, 1)
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
distinct = 0
i = 1
while le(i, len(aList)):
    seen = 0
    j = 1
    while lt(j, i):
        if eq(at(aList, j), at(aList, i)):
            seen = 1
        j = plus(j, 1)
    if eq(seen, 0):
        distinct = plus(distinct, 1)
    i = plus(i, 1)
say(cat("distinct=", distinct))
```

### T20
```
cDigits = "12345"
total = 0
i = 1
while le(i, len(cDigits)):
    total = plus(total, at(cDigits, i))
    i = plus(i, 1)
say(cat("sum=", total))
```
