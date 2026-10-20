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
third = at(aList, 3)
last = at(aList, len(aList))
say(cat(cat("third=", str(third)), cat(" last=", str(last))))
```

### T03
```
aItems = ["1", "01", "1.0", "x", 2]
count = 0
for x in aItems:
    if eq(x, 1):
        count = plus(count, 1)
say(cat("count=", str(count)))
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
line = ""
for i in span(1, n):
    if i == 1:
        line = str(i)
    else:
        line = cat(cat(line, " "), str(i))
say(line)
```

### T06
```
cText = "ring plus plus"
vowels = 0
for i in span(1, len(cText)):
    c = at(cText, i)
    if eq(c, "a") or eq(c, "e") or eq(c, "i") or eq(c, "o") or eq(c, "u"):
        vowels = plus(vowels, 1)
say(cat("vowels=", str(vowels)))
```

### T07
```
aList = [1, 2, 3, 4, 5]
line = ""
for i in span(len(aList), 1, -1):
    if i == len(aList):
        line = str(at(aList, i))
    else:
        line = cat(cat(line, " "), str(at(aList, i)))
say(line)
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
a = 1
b = 1
line = ""
for i in span(1, n):
    if i == 1:
        line = str(a)
    else:
        line = cat(cat(line, " "), str(a))
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
    def Value(self):
        return self.n

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
m = at(aList, 1)
for i in span(2, len(aList)):
    x = at(aList, i)
    if gt(x, m):
        m = x
say(cat("max=", str(m)))
```

### T13
```
cText = "the quick brown fox"
words = 0
inword = 0
for i in span(1, len(cText)):
    c = at(cText, i)
    if eq(c, " "):
        inword = 0
    else:
        if inword == 0:
            words = plus(words, 1)
        inword = 1
say(cat("words=", str(words)))
```

### T14
```
aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]
cWho = "bob"
age = 0
for p in aPeople:
    if eq(at(p, 1), cWho):
        age = at(p, 2)
say(cat("age=", str(age)))
```

### T15
```
n = 3
for i in span(1, n):
    line = ""
    for j in span(1, n):
        if j == 1:
            line = str(i * j)
        else:
            line = cat(cat(line, " "), str(i * j))
    say(line)
```

### T16
```
a = 7
b = 2
q = floor(a / b)
r = mod(a, b)
say(cat(cat("q=", str(q)), cat(" r=", str(r))))
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
distinct = 0
for i in span(1, len(aList)):
    x = at(aList, i)
    seen = 0
    for j in span(1, i - 1):
        if eq(at(aList, j), x):
            seen = 1
    if seen == 0:
        distinct = plus(distinct, 1)
say(cat("distinct=", str(distinct)))
```

### T20
```
cDigits = "12345"
total = 0
for i in span(1, len(cDigits)):
    total = plus(total, at(cDigits, i))
say(cat("sum=", str(total)))
```
