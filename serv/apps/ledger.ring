# an app whose handler makes objects of a class ANOTHER app brings, deployed
# after it (apps/entry.ring): the `new` is compiled before the class exists and
# finds it by name once that app is admitted -- the resident VM's rung 8
Route("GET", "/ledger", "LedgerNew")

func LedgerNew cBody
	oE = new Entry("rent", 40)
	return oE.Show()
