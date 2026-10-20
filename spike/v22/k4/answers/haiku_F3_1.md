### T01
```
n = 10
total = 0
if n >= 1:
    for i in span(1, n):
        total = plus(total, i)
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
sep = ""
if n >= 1:
    for i in span(1, n):
        line = cat(cat(line, sep), i)
        sep = " "
say(line)
```

### T06
```
cText = "ring plus plus"
vowels = 0
if len(cText) >= 1:
    for i in span(1, len(cText)):
        ch = at(cText, i)
        if eq(ch, "a") or eq(ch, "e") or eq(ch, "i") or eq(ch, "o") or eq(ch, "u"):
            vowels = plus(vowels, 1)
say(cat("vowels=", vowels))
```

### T07
```
aList = [1, 2, 3, 4, 5]
line = ""
sep = ""
for i in span(len(aList), 1, -1):
    line = cat(cat(line, sep), at(aList, i))
    sep = " "
say(line)
```

### T08
```
n = 6
fact = 1
if n >= 1:
    for i in span(1, n):
        fact = fact * i
say(cat("fact=", fact))
```

### T09
```
n = 10
line = ""
sep = ""
a = 1
b = 1
if n >= 1:
    for i in span(1, n):
        line = cat(cat(line, sep), a)
        sep = " "
        t = plus(a, b)
        a = b
        b = t
say(line)
```

### T10
```
nTimes = 3
c = new_without_init(Counter)
if nTimes >= 1:
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
if len(cText) >= 1:
    for i in span(1, len(cText)):
        ch = at(cText, i)
        if eq(ch, " "):
            inWord = 0
        elif inWord == 0:
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
if n >= 1:
    for i in span(1, n):
        line = ""
        sep = ""
        for j in span(1, n):
            line = cat(cat(line, sep), i * j)
            sep = " "
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
out = ""
if n >= 1:
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
distinct = 0
if len(aList) >= 1:
    for i in span(1, len(aList)):
        x = at(aList, i)
        seen = 0
        for j in span(1, i):
            if j < i:
                if eq(at(aList, j), x):
                    seen = 1
        if seen == 0:
            distinct = plus(distinct, 1)
say(cat("distinct=", distinct))
```

### T20
```
cDigits = "12345"
total = 0
if len(cDigits) >= 1:
    for i in span(1, len(cDigits)):
        ch = at(cDigits, i)
        for d in span(0, 9):
            if eq(ch, d):
                total = plus(total, d)
say(cat("sum=", total))
```
