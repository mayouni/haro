# live_gate_limits.ring -- three things stzRefinableCode does that its header does not say, measured on the Ring++ package for rung 20 (2026-10-05):
#
#     runtime/package/ringpp-win64/bin/rnxc.exe haro/spike/v20/probes/live_gate_limits.ring
#
#   1. its header says the STRUCTURAL stage checks that "the value parses"; the code checks that the point exists, so a value that is not a number reaches the CONSTRAINT
#      stage, whose ring_number() RAISES -- the proposal is not refused, the caller's program is stopped (Error (R41) : Invalid numeric string)
#   2. the tag form carries the value as value="...": a value holding a double quote is cut at it, and nothing says so (the point reads back `say `)
#   3. every rule of the program is evaluated on every proposal, so a program that already breaks one cannot be refined at all, whichever point is proposed
#
# The L1 gate (v20/refine.py) refuses 1 at its structural stage, writes a literal of its own so 2 cannot happen, and answers for the rules of the point it touched (3).
# Expected output, on Ring 1.27's semantics as the package runs them:
#     raised: Error (R41) : Invalid numeric string
#     value read back: [say ]
#     admitted: 0 (derivation: rule 'r' violated -- the rule is already broken, and this is another point)

load "stzlib.ring"

o = new stzRefinableCode('x = <R:PARAM name="vat" value="0.20" min="0" max="0.9">')
try
	r = o.Refine("vat").To("abc")
	? "answered: " + r[:admitted] + " " + r[:why]
catch
	? "raised: " + cCatchError
done

o2 = new stzRefinableCode('x = <R:PARAM name="label" value="say ' + '"hi"' + '">')
? "value read back: [" + o2.ValueOf("label") + "]"

o3 = new stzRefinableCode('x = <R:PARAM name="a" value="1">' + nl + 'x = <R:PARAM name="b" value="9">' + nl + 'x = <R:PARAM name="c" value="5" max="10">')
o3.DeclareDerivation("r", func oCode { return ring_number(oCode.ValueOf("a")) >= ring_number(oCode.ValueOf("b")) }, "the rule is already broken, and this is another point")
r3 = o3.Refine("c").To("6")
? "admitted: " + r3[:admitted] + " (" + r3[:why] + ")"
