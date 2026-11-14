"""v0.48: the one spelling of each Ring built-in in a .haro file -- Softanza's casing, the Principal's ruling of 2026-11-09 ("ParentClassName",
revising the 2026-11-07 "Lowercase (Recommended)"). The table is drawn here by a stated rule, the desk's reading under the Principal's
delegation ("I let you decide", 2026-11-09), and counted against Haro's own code.

THE RULE: the name is split into the English words it is made of and each word is capitalised -- parentclassname ParentClassName, isnull
IsNull, substr SubStr (Ring's own word: sub-string), addattribute AddAttribute; a digit stays where it stands and starts no word
(list2str List2Str, atan2 Atan2, log10 Log10); a C library name keeps C's reading with each part a word (fopen FOpen: the F is "file",
fgetc FGetC, ungetc UnGetC, clearerr ClearErr, perror PError, fabs FAbs); Ring's two internal prefixes are words of their own
(ring_state_new RingStateNew, ringvm_callfunc RingVMCallFunc) -- the underscore goes, as no other Softanza name carries one.
Every split is written below, by hand, once: a dictionary guess is no rule.

  python study/v48/builtin_names.py            the table, with each built-in's calls in Haro's code
  python study/v48/builtin_names.py --zig      the table as compile.zig's array
"""
import glob, os, re, sys, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# every one of builtins.zig's 258 names, split by hand: the words, joined
SPLIT = """
acos A-Cos | add Add | addattribute Add-Attribute | adddays Add-Days | addmethod Add-Method | ascii Ascii
asin A-Sin | assert Assert | atan A-Tan | atan2 A-Tan2 | attributes Attributes | binarysearch Binary-Search
bytes2double Bytes2-Double | bytes2float Bytes2-Float | bytes2int Bytes2-Int | callgarbagecollector Call-Garbage-Collector | callgc Call-GC | ceil Ceil
cfunctions C-Functions | char Char | chdir Ch-Dir | checkoverflow Check-Overflow | classes Classes | classname Class-Name
clearerr Clear-Err | clock Clock | clockspersecond Clocks-Per-Second | closelib Close-Lib | copy Copy | cos Cos
cosh CosH | currentdir Current-Dir | date Date | dec Dec | decimals Decimals | del Del
diffdays Diff-Days | dir Dir | direxists Dir-Exists | double2bytes Double2-Bytes | eval Eval | exefilename Exe-File-Name
exefolder Exe-Folder | exp Exp | fabs F-Abs | fclose F-Close | feof F-EOF | ferror F-Error
fexists F-Exists | fflush F-Flush | fgetc F-Get-C | fgetpos F-Get-Pos | fgets F-Gets | filename File-Name
find Find | float2bytes Float2-Bytes | floor Floor | fopen F-Open | fputc F-Put-C | fputs F-Puts
fread F-Read | freopen F-Reopen | fseek F-Seek | fsetpos F-Set-Pos | ftell F-Tell | functions Functions
fwrite F-Write | getarch Get-Arch | getattribute Get-Attribute | getchar Get-Char | getfilesize Get-File-Size | getnumber Get-Number
getpathtype Get-Path-Type | getpointer Get-Pointer | getptr Get-Ptr | getstring Get-String | globals Globals | hex Hex
hex2str Hex2-Str | importpackage Import-Package | input Input | insert Insert | int2bytes Int2-Bytes | intvalue Int-Value
isalnum Is-Alnum | isalpha Is-Alpha | isandroid Is-Android | isattribute Is-Attribute | iscfunction Is-C-Function | isclass Is-Class
iscntrl Is-Cntrl | isdigit Is-Digit | isfreebsd Is-FreeBSD | isfunction Is-Function | isglobal Is-Global | isgraph Is-Graph
islinux Is-Linux | islist Is-List | islocal Is-Local | islower Is-Lower | ismacosx Is-MacOSX | ismethod Is-Method
ismsdos Is-MSDOS | isnull Is-Null | isnumber Is-Number | isobject Is-Object | ispackage Is-Package | ispackageclass Is-Package-Class
ispointer Is-Pointer | isprint Is-Print | isprivateattribute Is-Private-Attribute | isprivatemethod Is-Private-Method | ispunct Is-Punct | isspace Is-Space
isstring Is-String | isunix Is-Unix | isupper Is-Upper | iswindows Is-Windows | iswindows64 Is-Windows64 | isxdigit Is-XDigit
left Left | len Len | lines Lines | list List | list2str List2-Str | loadlib Load-Lib
locals Locals | log Log | log10 Log10 | lower Lower | max Max | memcpy Mem-Cpy
memorycopy Memory-Copy | mergemethods Merge-Methods | methods Methods | min Min | murmur3hash Murmur3-Hash | newlist New-List
nofprocessors N-Of-Processors | nothing Nothing | nullpointer Null-Pointer | nullptr Null-Ptr | number Number | obj2ptr Obj2-Ptr
object2pointer Object2-Pointer | objectid Object-ID | optionalfunc Optional-Func | packageclasses Package-Classes | packagename Package-Name | packages Packages
parentclassname Parent-Class-Name | perror P-Error | pointer2object Pointer2-Object | pointer2string Pointer2-String | pointercompare Pointer-Compare | pow Pow
prevfilename Prev-File-Name | print Print | print2str Print2-Str | ptr2obj Ptr2-Obj | ptr2str Ptr2-Str | ptrcmp Ptr-Cmp
puts Puts | raise Raise | random Random | randomize Randomize | read Read | ref Ref
refcount Ref-Count | reference Reference | remove Remove | rename Rename | reverse Reverse | rewind Rewind
right Right | ring_give Ring-Give | ring_see Ring-See | ring_state_delete Ring-State-Delete | ring_state_filetokens Ring-State-File-Tokens | ring_state_findvar Ring-State-Find-Var
ring_state_init Ring-State-Init | ring_state_main Ring-State-Main | ring_state_mainfile Ring-State-Main-File | ring_state_new Ring-State-New | ring_state_newvar Ring-State-New-Var | ring_state_resume Ring-State-Resume
ring_state_runcode Ring-State-Run-Code | ring_state_runcodeatins Ring-State-Run-Code-At-Ins | ring_state_runfile Ring-State-Run-File | ring_state_runobjectfile Ring-State-Run-Object-File | ring_state_scannererror Ring-State-Scanner-Error | ring_state_setvar Ring-State-Set-Var
ring_state_stringtokens Ring-State-String-Tokens | ringvm_callfunc RingVM-Call-Func | ringvm_calllist RingVM-Call-List | ringvm_cfunctionslist RingVM-C-Functions-List | ringvm_classeslist RingVM-Classes-List | ringvm_codelist RingVM-Code-List
ringvm_evalinscope RingVM-Eval-In-Scope | ringvm_fileslist RingVM-Files-List | ringvm_functionslist RingVM-Functions-List | ringvm_genarray RingVM-Gen-Array | ringvm_give RingVM-Give | ringvm_hideerrormsg RingVM-Hide-Error-Msg
ringvm_info RingVM-Info | ringvm_ismempool RingVM-Is-Mem-Pool | ringvm_memorylist RingVM-Memory-List | ringvm_packageslist RingVM-Packages-List | ringvm_passerror RingVM-Pass-Error | ringvm_ringolists RingVM-Ringo-Lists
ringvm_runcode RingVM-Run-Code | ringvm_scopescount RingVM-Scopes-Count | ringvm_see RingVM-See | ringvm_settrace RingVM-Set-Trace | ringvm_tracedata RingVM-Trace-Data | ringvm_traceevent RingVM-Trace-Event
ringvm_tracefunc RingVM-Trace-Func | ringvm_translatecfunction RingVM-Translate-C-Function | ringvm_writeringo RingVM-Write-Ringo | setattribute Set-Attribute | setpointer Set-Pointer | setptr Set-Ptr
shutdown Shutdown | sin Sin | sinh SinH | sort Sort | space Space | sqrt Sqrt
srandom S-Random | str2hex Str2-Hex | str2hexcstyle Str2-Hex-C-Style | str2list Str2-List | strcmp Str-Cmp | string String
substr Sub-Str | swap Swap | sysget Sys-Get | sysset Sys-Set | syssleep Sys-Sleep | system System
sysunset Sys-Unset | tan Tan | tanh TanH | tempfile Temp-File | tempname Temp-Name | time Time
timelist Time-List | trim Trim | type Type | ungetc Un-Get-C | unsigned Unsigned | upper Upper
uptime Up-Time | variablepointer Variable-Pointer | varptr Var-Ptr | version Version | windowsnl Windows-NL | write Write
"""
# the VM's own natives (compile.zig's builtin_table, beyond Ring's 258): the resident VM's, the terminal's, the browser's -- one rule for
# every native the VM registers (the desk's reading)
SPLIT_VM = """
admitapp Admit-App | admitcode Admit-Code | admitfile Admit-File | admitfinish Admit-Finish | admitstart Admit-Start | admitstate Admit-State
releasecode Release-Code | releasefile Release-File | replaceapp Replace-App | replacecode Replace-Code | replacefile Replace-File
tui_done TUI-Done | tui_init TUI-Init | tui_key TUI-Key | tui_size TUI-Size | web_bye Web-Bye | web_done Web-Done | web_serve Web-Serve
web_wait Web-Wait | systemcmd System-Cmd | systemrun System-Run
decimal Decimal | divide Divide | float Float | integer Integer | near Near
text Text | round Round | integerpart Integer-Part | decimalpart Decimal-Part | digits Digits | abs Abs | sign Sign | clamp Clamp
fromhex From-Hex
keys Keys | values Values | haskey Has-Key
makedir Make-Dir
"""


def table():
    out = {}
    for cell in re.split(r"[|\n]", SPLIT + SPLIT_VM):
        cell = cell.strip()
        if not cell:
            continue
        low, split = cell.split()
        parts = split.split("-")
        name = "".join(p[0].upper() + p[1:] for p in parts)
        assert name.lower() == low.replace("_", ""), (low, name)
        out[low] = name
    return out


def zig_names():
    src = open(os.path.join(ROOT, "vm", "src", "builtins.zig"), encoding="utf-8").read()
    body = src[src.index("pub const names"):src.index("};", src.index("pub const names"))]
    return re.findall(r'"([a-z0-9_]+)"', body)


def code_calls():
    sys.path.insert(0, os.path.join(ROOT, "study", "v47"))
    import reletter as R
    c = collections.Counter()
    for rel in R.code_files():
        toks = R.tokens(open(os.path.join(ROOT, rel), encoding="utf-8").read())
        for i, (k, v) in enumerate(toks):
            if k != "id":
                continue
            j = R.sig(toks, i, 1)
            if j is not None and toks[j][1] == "(" and not R.is_member(toks, i):
                c[v] += 1
    return c


if __name__ == "__main__":
    t = table()
    names = zig_names()
    vm_own = [c.split()[0] for c in re.split(r"[|\n]", SPLIT_VM) if c.strip()]
    missing = sorted(set(names) - set(t))
    extra = sorted(set(t) - set(names) - set(vm_own))
    assert not missing and not extra, (missing, extra)
    if "--zig" in sys.argv:
        for low in names + vm_own:
            print(f'    .{{ "{low}", "{t[low]}" }},')
        sys.exit(0)
    calls = code_calls()
    used = [(sum(n for k, n in calls.items() if k.lower() == low), low) for low in names]
    print(f"{len(names)} built-ins; {sum(1 for n, _ in used if n)} called in Haro's .haro code, {sum(n for n, _ in used)} calls")
    for n, low in sorted(used, reverse=True):
        if n:
            print(f"  {n:5d}  {low:24s} -> {t[low]}")
