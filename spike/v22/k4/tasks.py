"""The K4 tasks (rung 7 of the code-graph memo, kill criterion K4): twenty small programs, each stated in plain English, each with a reference solution in Ring.

A task has a PREAMBLE -- the line(s) a program must begin with, which hold its data -- and a variant of the data the checker substitutes (so a program that prints the
shown answer instead of computing it fails). The reference solution is Ring written for the oracle; its output on the shown data goes into the statement, its output on
the hidden data is what a candidate must also print. Every reference is also printed through the face and read back (k4.py build): a task the face cannot say would not
be a test of the face.

The tasks lean on what the face was made for -- 1-based positions, Ring's `=` between a string and a number, `+` that joins, the remainder, a loop's inclusive bound,
and/or/not as values, classes with a region, try/catch -- and include easy ones, so that a ceiling does not hide a difference.
"""

TASKS = [
    {
        'id': 'T01', 'text': 'Print the sum of the integers from 1 to n (inclusive) as `sum=<value>`.',
        'a': ['n = 10'], 'b': ['n = 7'],
        'ref': '''nSum = 0
for i = 1 to n
	nSum = nSum + i
next
? "sum=" + nSum
''',
    },
    {
        'id': 'T02', 'text': 'Print the third element of the list and its last element on one line, as `third=<x> last=<y>`.',
        'a': ['aList = [10, 20, 30, 40]'], 'b': ['aList = [5, 6, 7, 8, 9]'],
        'ref': '''? "third=" + aList[3] + " last=" + aList[len(aList)]
''',
    },
    {
        'id': 'T03', 'text': ('Print how many items of the list are numerically equal to 1, as `count=<n>`. A string item counts when its numeric value is 1 '
                              '(so "01" and "1.0" count); a string that is not a number never counts.'),
        'a': ['aItems = ["1", "01", "1.0", "x", 2]'], 'b': ['aItems = ["1", 1, "01", "1.0", "1.00", "7"]'],
        'ref': '''nCount = 0
for i = 1 to len(aItems)
	if aItems[i] = 1
		nCount++
	ok
next
? "count=" + nCount
''',
    },
    {
        'id': 'T04', 'text': 'Print the name and the number joined by a dash, as `<name>-<number>`.',
        'a': ['cName = "item"', 'n = 5'], 'b': ['cName = "box"', 'n = 12'],
        'ref': '''? cName + "-" + n
''',
    },
    {
        'id': 'T05', 'text': 'Print the integers from 1 to n on a single line, separated by single spaces, with no trailing space.',
        'a': ['n = 5'], 'b': ['n = 8'],
        'ref': '''cLine = ""
for i = 1 to n
	if i > 1
		cLine = cLine + " "
	ok
	cLine = cLine + i
next
? cLine
''',
    },
    {
        'id': 'T06', 'text': 'Count the vowels (the characters a, e, i, o, u) in the text and print `vowels=<n>`. The text is lower case.',
        'a': ['cText = "ring plus plus"'], 'b': ['cText = "banana split"'],
        'ref': '''nV = 0
for i = 1 to len(cText)
	c = cText[i]
	if c = "a" or c = "e" or c = "i" or c = "o" or c = "u"
		nV++
	ok
next
? "vowels=" + nV
''',
    },
    {
        'id': 'T07', 'text': 'Print the elements of the list in reverse order on a single line, separated by single spaces.',
        'a': ['aList = [1, 2, 3, 4, 5]'], 'b': ['aList = [9, 8, 1]'],
        'ref': '''cOut = ""
for i = len(aList) to 1 step -1
	if cOut != ""
		cOut = cOut + " "
	ok
	cOut = cOut + aList[i]
next
? cOut
''',
    },
    {
        'id': 'T08', 'text': 'Print the factorial of n as `fact=<value>`.',
        'a': ['n = 6'], 'b': ['n = 5'],
        'ref': '''nF = 1
for i = 2 to n
	nF = nF * i
next
? "fact=" + nF
''',
    },
    {
        'id': 'T09', 'text': 'Print the first n Fibonacci numbers (1 1 2 3 5 ...) on a single line, separated by single spaces.',
        'a': ['n = 10'], 'b': ['n = 6'],
        'ref': '''a = 1
b = 1
cOut = ""
for i = 1 to n
	if i > 1
		cOut = cOut + " "
	ok
	cOut = cOut + a
	t = a + b
	a = b
	b = t
next
? cOut
''',
    },
    {
        'id': 'T10', 'text': ('Define a class Counter whose objects hold a count that starts at 0, with a method Add that adds 1 and a method Value that returns the count. '
                              'Create one object, call Add nTimes times, and print `count=<n>`.'),
        'a': ['nTimes = 3'], 'b': ['nTimes = 5'],
        'ref': '''o = new Counter
for i = 1 to nTimes
	o.Add()
next
? "count=" + o.Value()

class Counter
	n = 0

	func Add()
		This.n = This.n + 1

	func Value()
		return This.n
''',
    },
    {
        'id': 'T11', 'text': ('Call a function named Missing, which is not defined anywhere, inside a protected block (try/catch). When it fails, print `caught-` followed by '
                              'the tag; after the protected block, print `done`.'),
        'a': ['cTag = "x"'], 'b': ['cTag = "yz"'],
        'ref': '''try
	Missing()
catch
	? "caught-" + cTag
done
? "done"
''',
    },
    {
        'id': 'T12', 'text': 'Print the largest element of the list as `max=<x>`. Do not use a built-in maximum function; the list may hold negative numbers.',
        'a': ['aList = [3, 9, 2, 7]'], 'b': ['aList = [-5, -2, -9]'],
        'ref': '''nMax = aList[1]
for i = 2 to len(aList)
	if aList[i] > nMax
		nMax = aList[i]
	ok
next
? "max=" + nMax
''',
    },
    {
        'id': 'T13', 'text': 'Count the words of the text -- maximal runs of characters other than a space -- and print `words=<n>`.',
        'a': ['cText = "the quick brown fox"'], 'b': ['cText = "  two   words "'],
        'ref': '''nW = 0
bIn = 0
for i = 1 to len(cText)
	if cText[i] != " "
		if bIn = 0
			nW++
			bIn = 1
		ok
	else
		bIn = 0
	ok
next
? "words=" + nW
''',
    },
    {
        'id': 'T14', 'text': 'The list holds [name, age] pairs. Print the age of the person named cWho as `age=<n>`.',
        'a': ['aPeople = [["ann", 31], ["bob", 27], ["cy", 45]]', 'cWho = "bob"'], 'b': ['aPeople = [["dee", 19], ["eli", 52]]', 'cWho = "eli"'],
        'ref': '''for i = 1 to len(aPeople)
	if aPeople[i][1] = cWho
		? "age=" + aPeople[i][2]
	ok
next
''',
    },
    {
        'id': 'T15', 'text': 'Print a multiplication table with n rows: row i holds i*1, i*2, ... i*n, separated by single spaces.',
        'a': ['n = 3'], 'b': ['n = 4'],
        'ref': '''for i = 1 to n
	cRow = ""
	for j = 1 to n
		if j > 1
			cRow = cRow + " "
		ok
		cRow = cRow + (i * j)
	next
	? cRow
next
''',
    },
    {
        'id': 'T16', 'text': 'Print the quotient of a divided by b, rounded down, and the remainder, as `q=<q> r=<r>`.',
        'a': ['a = 7', 'b = 2'], 'b': ['a = 9', 'b = 4'],
        'ref': '''? "q=" + floor(a / b) + " r=" + (a % b)
''',
    },
    {
        'id': 'T17', 'text': 'Print the piece repeated n times, with nothing between the copies.',
        'a': ['cPiece = "ab"', 'n = 3'], 'b': ['cPiece = "x"', 'n = 5'],
        'ref': '''cOut = ""
for i = 1 to n
	cOut = cOut + cPiece
next
? cOut
''',
    },
    {
        'id': 'T18', 'text': 'Print `out=1` if a is greater than b and b is not equal to 5, otherwise print `out=0`.',
        'a': ['a = 3', 'b = 2'], 'b': ['a = 1', 'b = 5'],
        'ref': '''nOut = 0
if a > b and not b = 5
	nOut = 1
ok
? "out=" + nOut
''',
    },
    {
        'id': 'T19', 'text': 'Print the number of distinct values in the list as `distinct=<n>`.',
        'a': ['aList = [1, 2, 2, 3, 3, 3]'], 'b': ['aList = [7, 8, 9, 7, 8, 1]'],
        'ref': '''nD = 0
for i = 1 to len(aList)
	bSeen = 0
	for j = 1 to i - 1
		if aList[j] = aList[i]
			bSeen = 1
		ok
	next
	if bSeen = 0
		nD++
	ok
next
? "distinct=" + nD
''',
    },
    {
        'id': 'T20', 'text': 'Print the sum of the digits of the string, as `sum=<n>`.',
        'a': ['cDigits = "12345"'], 'b': ['cDigits = "909"'],
        'ref': '''nS = 0
for i = 1 to len(cDigits)
	nS = nS + cDigits[i]
next
? "sum=" + nS
''',
    },
]
