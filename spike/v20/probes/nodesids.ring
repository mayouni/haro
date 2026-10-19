load "stzlib.ring"
try
o = new stzRefinableCode('x = <R:PARAM name="vat" value="0.20" min="0" max="0.9">' + nl + 'x = <R:PARAM name="floor" value="0.10" min="0" max="0.5">' + nl + 'x = <R:ALGO name="sort" value="quick" options="quick|merge|heap">')
o.SetGovernedBy(new stzGovernance("ops"))
o.SetActor("intern")
o.SetRiskFor("vat", 1)
o.SetRiskFor("floor", 2)
o.SetRiskFor("sort", 3)
o.SetAllowRefine("vat")
o.SetAuthorityLevel(:Advisory)
o.TrustFloor("floor", "external")
o.TrustFloor("sort", "trusted")
o.DeclareDerivation("vat-above-floor", func oCode { return ring_number(oCode.ValueOf("vat")) >= ring_number(oCode.ValueOf("floor")) }, "vat must not drop below floor")
o.DeclareDerivation("floor-cap", func oCode { return ring_number(oCode.ValueOf("floor")) <= ring_number("0.3") }, "floor is capped at 0.3")
r = o.Refine("vat").As("sandboxed").To("-0.1")
? "V|150|" + r[:admitted] + "|" + r[:why] + "|" + o.ValueOf("vat")
catch
? "V|150|ERR|" + cCatchError + "|"
done
try
o = new stzRefinableCode('x = <R:PARAM name="vat" value="0.20" min="0" max="0.9">' + nl + 'x = <R:PARAM name="floor" value="0.10" min="0" max="0.5">' + nl + 'x = <R:ALGO name="sort" value="quick" options="quick|merge|heap">')
o.SetGovernedBy(new stzGovernance("ops"))
o.SetActor("boss")
o.SetRiskFor("vat", 1)
o.SetRiskFor("floor", 2)
o.SetRiskFor("sort", 3)
o.SetAllowRefine("vat")
o.SetAllowRefine("floor")
o.SetAllowRefine("sort")
o.SetAuthorityLevel(:EmergencyOverride)
o.TrustFloor("floor", "external")
o.TrustFloor("sort", "trusted")
o.DeclareDerivation("vat-above-floor", func oCode { return ring_number(oCode.ValueOf("vat")) >= ring_number(oCode.ValueOf("floor")) }, "vat must not drop below floor")
o.DeclareDerivation("floor-cap", func oCode { return ring_number(oCode.ValueOf("floor")) <= ring_number("0.3") }, "floor is capped at 0.3")
r = o.Refine("vat").As("trusted").To("-0.1")
? "V|152|" + r[:admitted] + "|" + r[:why] + "|" + o.ValueOf("vat")
catch
? "V|152|ERR|" + cCatchError + "|"
done
try
o = new stzRefinableCode('x = <R:PARAM name="vat" value="0.20" min="0" max="0.9">' + nl + 'x = <R:PARAM name="floor" value="0.10" min="0" max="0.5">' + nl + 'x = <R:ALGO name="sort" value="quick" options="quick|merge|heap">')
o.SetGovernedBy(new stzGovernance("ops"))
o.SetActor("bot")
o.SetRiskFor("vat", 1)
o.SetRiskFor("floor", 2)
o.SetRiskFor("sort", 3)
o.SetAllowRefine("vat")
o.SetAllowRefine("floor")
o.SetAllowRefine("sort")
o.SetAuthorityLevel(:Delegated)
o.TrustFloor("floor", "external")
o.TrustFloor("sort", "trusted")
o.DeclareDerivation("vat-above-floor", func oCode { return ring_number(oCode.ValueOf("vat")) >= ring_number(oCode.ValueOf("floor")) }, "vat must not drop below floor")
o.DeclareDerivation("floor-cap", func oCode { return ring_number(oCode.ValueOf("floor")) <= ring_number("0.3") }, "floor is capped at 0.3")
r = o.Refine("vat").As("external").To("0.05")
? "V|161|" + r[:admitted] + "|" + r[:why] + "|" + o.ValueOf("vat")
catch
? "V|161|ERR|" + cCatchError + "|"
done

# A reproduction found by v20/refine_check.py (2026-10-05): three objects built one after another on the Ring++ package, the third reaching its
# derivation rules, raise `Error (R14) : Calling Method without definition: nodesids` -- a method nothing in stzRefinableCode calls. Run alone, the
# third case answers correctly; run with either of the first two missing, the same. Cases 150, 152 and 161 of the court's live-gate sweep, as generated.
#
#     runtime/package/ringpp-win64/bin/rnxc.exe haro/spike/v20/probes/nodesids.ring
#
# Expected (what Ring answers, and what the third case answers alone): V|161|0|derivation: rule 'vat-above-floor' violated -- vat must not drop below floor|0.20
# NOTE: the same file with these comment lines at its TOP does not raise -- any byte above case 161 moves it, which is what the cause is.
# DIAGNOSED 2026-10-05: the Ring++ package's compiler was a copy of 2026-09-28 and found a lambda by its byte offset across every file of the unit; the derivation
# lambda of case 161 starts at byte 2557 of this file, and base/security/stzSecurityRule.ring has a lambda at byte 2557, `func oGraph { ... oGraph.NodesIds() ... }`,
# which ran in its place. Fixed by bc47ddb (the lookup matches the file as well as the offset); this file answers correctly on any compiler since, the packages laid out
# since 2026-10-13 included. The pin is bench/exec/lambda_offset.ring; the account is in CLAUDE.md.
