# an app whose handler makes objects of a class ANOTHER app brings, deployed
# after it (apps/entry.ring, which exports Entry): the `new` is compiled before
# the class exists and finds it by its public name, `entry.Entry`, once that app
# is admitted -- the resident VM's rung 8, under D31's namespaces
Route("GET", "/ledger", "LedgerNew")

func LedgerNew cBody
	oE = new entry.Entry("rent", 40)
	return oE.Show()
