# Haro's numbers -- what the language itself carries

A proposal for the Principal's ruling, 2026-11-12 (HARO-NUMBERS-CORE-01) -- **RULED "Build it as proposed" and BUILT as v0.66 (D78)**, with one departure said so in D78: `Truncate` is not built, as it answers what `IntegerPart` answers. Its occasion is his ruling of the same day:

> Haro should not embrace the vague semantics of [the classic surface], for example in naming decimals(n) ... Haro should not
> reproduce the wrong design of ... changing the decimals globally. ... if we need the decimals(10.257) we get a list [2, 5, 7], if we
> want the decimal part we say DecimalPart(10.257) and we get 0.257. Look at how we designed this in Softanza number staff, and rethink
> the scope of Haro and what it should be basically supported in the language. This should be sufficient to common uses (should not
> load softanza just to get basic things). Also we should learn from the best designed languages.

TYPES.md (D55) gave Haro its number types: `i` an exact integer, `d` an exact decimal that keeps its scale (`12.50`), `f` a float
(`0.5f`), `n` any of the three; v0.52 made them so. This file settles **what a `.haro` program can do with a number without loading
anything**. A `.ring` file keeps the classic surface as it is (D54).

---

## 1. What is wrong today, measured on haro 8b01e8a+ (the installed v0.65)

    print 1.0f / 3.0f        # 0.33          -- a float written with two places: what it holds is lost
    Decimals(5)              # a setting for the whole process, from any file, any library
    print 1.0f / 3.0f        # 0.33333       -- the same line, another answer
    print String(0.1f)       # 0.10000       -- and every text of a float after it

The inherited surface has one process-wide number of places, `Decimals(n)`, read by every print and every number made text. A library
that sets it changes what its caller prints; a caller that sets it changes what the library writes into a file. It is the shape of a
global the Principal named: what led away from the classic surface must not stand in Haro.

---

## 2. What the best-designed languages agree on

| | Python | Rust | Swift | Java | C# |
|---|---|---|---|---|---|
| a float's default text | shortest text that reads back the same (`repr`, since 3.1) | the same (`{}`) | the same | the same (`Double.toString`) | the same (since .NET Core 3.0) |
| places | per value: `f"{x:.2f}"`, `round(x, 2)` | per value: `{:.2}` | per value: `.formatted(.number.precision(.fractionLength(2)))` | per value: `setScale(2, mode)`, `String.format` | per value: `Math.Round(x, 2, mode)`, `x.ToString("F2")` |
| a process-wide setting for places | none | none | none | none | none |
| how a tie rounds | half to even (`round`) | named: `round` away from zero, `round_ties_even` | named rule, `.toNearestOrEven` and others | named `RoundingMode` | named `MidpointRounding` |
| the parts of a number | `math.modf`, `math.trunc` | `trunc`, `fract` | `rounded(.towardZero)` | `BigDecimal.scale()`, `unscaledValue()` | `Math.Truncate` |
| an exact decimal's digits | `Decimal.as_tuple()`: sign, digits, exponent | -- | -- | `unscaledValue`, `scale` | -- |

Four lessons, each one the language's own, never a library's:

1. **A float is written so it reads back the same** -- the shortest such text. Nothing it holds is dropped by printing it.
2. **Places are asked for per value**, at the place the text is made. No language among them has a setting a library can change for
   its caller.
3. **A tie's rule is named**, and one rule is the default. Haro already rounds half to even (`Divide`, v0.52): the same rule
   everywhere, and no mode to pass.
4. **The parts of a number are functions with exact names** -- an integer part, a decimal part, the digits -- and an exact decimal keeps
   its scale, so its digits are what was written.

---

## 3. Softanza's names, which Haro takes

Softanza's `stzNumber` (stzlib origin/main e62962f89, `base/number/stzNumber.ring`) already names these exactly, and the Principal's
example is its own: `Decimals()` is the list of the digits after the point (`[2, 5, 7]` for 10.257), `Integers()` the digits before it,
`Digits()` all of them, `DecimalPart()` and `IntegerPart()` the parts, `RoundedTo(n)` a rounding per value. Haro's built-ins take those
names where they name a basic thing, one spelling each (`FractionalPart`, `DecimalPartValue` and the other alternatives stay Softanza's).

---

## 4. The proposal: Haro's number built-ins

In a `.haro` file. "Same kind" means: an integer stays an integer, a decimal a decimal, a float a float.

**Written as text -- no setting anywhere**

| call | answers |
|---|---|
| `print x`, `String(x)` | an integer its digits; a decimal its digits as held (`12.50`); a float the shortest text that reads back the same (`0.1`, `0.3333333333333333`) |
| `Text(x, iPlaces)` | the text of x with exactly iPlaces after the point, the last place rounded half to even: `Text(2.5, 2)` is `"2.50"`, `Text(1.0f / 3.0f, 4)` is `"0.3333"` |

**Rounded -- per value, one rule (half to even, as `Divide`)**

| call | answers |
|---|---|
| `Round(x)` | the nearest integer, a tie to the even one: `Round(2.5)` is 2, `Round(3.5)` is 4 |
| `Round(x, iPlaces)` | x rounded to iPlaces, same kind: `Round(10.257, 2)` is 10.26 (a decimal of scale 2) |
| `Floor(x)`, `Ceil(x)`, `Truncate(x)` | the integer below, above, toward zero |

**Its parts and its digits**

| call | answers |
|---|---|
| `IntegerPart(x)` | the integer part, toward zero: `IntegerPart(10.257)` is 10, `IntegerPart(-10.257)` is -10 |
| `DecimalPart(x)` | what follows the point, same kind and sign: `DecimalPart(10.257)` is 0.257, `DecimalPart(-10.257)` is -0.257 |
| `Decimals(x)` | the digits after the point, a vector of integers: `Decimals(10.257)` is `[2, 5, 7]`; a decimal's as held (`Decimals(3.50)` is `[5, 0]`); a float's from its shortest text; an integer's is `[]` |
| `Digits(x)` | every digit, the integer part's then the decimals: `Digits(10.257)` is `[1, 0, 2, 5, 7]` |

**Sign, size, bounds**

| call | answers |
|---|---|
| `Abs(x)` | the absolute value, same kind (in place of `FAbs`, which took only a float) |
| `Sign(x)` | -1, 0 or 1, an integer |
| `Min(x, y)`, `Max(x, y)` | as today |
| `Clamp(x, lo, hi)` | x held between lo and hi |

**Kept as they are**: `Decimal`, `Float`, `Integer` (the conversions, v0.52), `Divide(a, b, iPlaces)`, `Near(a, b, f)`, `Sqrt`, `Pow`,
`Exp`, `Log`, `Log10`, the trigonometric functions, `Random`.

**Refused in a `.haro` file, each naming what to write**

| written | refused, naming |
|---|---|
| `Decimals(iN)` as a setting | there is no setting for places: `Text(x, iPlaces)` or `Round(x, iPlaces)` -- and `Decimals(x)` is the digits after the point |
| `FAbs(x)` | `Abs(x)` |
| `Dec(t)` (hex text to a number -- the name says decimal) | `FromHex(t)`, beside `Hex(i)` |

What a `.ring` file reads does not change: its `decimals(n)` still sets what its own code prints (v0.65 reads a `.haro` decimal there
as the classic number). A `.haro` file never reads that setting.

---

## 5. What stays in Softanza

Softanza's `stzNumber` keeps the rich domain: bases (binary, octal, hex forms of a part), scientific notation, the fluent and
alternative forms, statistics over lists of numbers, complex numbers, matrices. Haro carries what a program needs to compute and write a
number exactly; a program loads Softanza for a domain, never to print a price or take a number apart.

**Shadowing, said now**: stzlib defines global functions `Round(pxNumber)`, `Abs(xN)`, `Sign(xN)` (core/common), `Text(pcStr)` and
`Digits()` (stzlib origin/main e62962f89). A program's own function of a built-in's name is the program's (as `Divide` is shadowed today,
HARO-DIVIDE-SHADOWED-01), so stzlib keeps its meaning inside stzlib; the stzlib desk decides whether its globals give way to the
built-ins.

---

## 6. How it is built

One rung, fixtures first, both builds byte for byte, every protection planted, counted on stzlib's landed `.haro` files before the
shared haro.exe changes:

1. a float's text in a `.haro` file: the shortest that reads back the same; no `.haro` code reads the process setting;
2. `Text`, `Round`, `Truncate`, `IntegerPart`, `DecimalPart`, `Decimals`, `Digits`, `Abs`, `Sign`, `Clamp`, `FromHex`;
3. the refusals of `Decimals` as a setting, `FAbs` and `Dec`;
4. haroport: `decimals(n)` in a ported tree is named for its writer to rewrite (where a program relied on the setting, the places move
   to the values it writes).
