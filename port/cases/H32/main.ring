o = new P
o.FillQ(1).StrokeQ(2).
  AddRect(3)
o.Name().
see "x"
class P
func FillQ n return self
func StrokeQ n return self
func AddRect n see n
func Name return "p"
