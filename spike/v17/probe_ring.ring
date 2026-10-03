# probe_ring.ring -- core-Ring behaviours n_lib.ring relies on, asked of both runtimes before it was written.
# python: run it on rnxc and on the oracle; the two outputs must be identical.

? "ci-eq " + ("Abc" = "aBC")
? "ne " + ("abc" != "abd")
? "substr-replace " + substr("a,b,,c", ",", " ")
? "lower-utf8 " + lower("D" + char(195) + char(169) + "P")
? "ascii-hi " + ascii(char(195)) + " " + ascii(char(169))
? "upper " + upper("trésorier")
? "len-utf8 " + len("é")
? "find-str " + find(["a", "b", "c"], "b")
? "find-miss " + find(["a", "b"], "z")
cL = ["x", "y"]
cL + "z"
? "append " + len(cL)
? "left " + left("abcdef", 3) + " mid " + substr("abcdef", 3) + " mid2 " + substr("abcdef", 2, 3)
? "substr-find " + substr("abcdef", "cd")
? "nl " + len(nl)
? "isdigit " + isdigit("5") + " " + isdigit("a")
? "exe " + (len(exefilename()) > 0)
? "trim " + len(trim("  ab  "))
aPair = ["k", "v", "string"]
? "pair " + aPair[1] + aPair[2]
? "upper-char " + upper("a") + lower("A")
? "ci-find " + find(["Abc"], "abc")
