"""Every protection of v0.53 (the classic Ring surface's 1 and 0, TYPES.md section 6, D65) switched off in turn: the court must fail, for the
fixture that protection exists for. Each plant is text substitutions in vm/src (main.zig, compile.zig), built into runtime/v53/plant-build
(ReleaseFast, -j2, one build at a time), the court run on that build alone, the files restored byte for byte -- verified by their digests,
and restored even when a build fails or the script is stopped.

Not planted, said so: boolExpr's `self.haroNode(n)` -- in a .ring file a converted 1 and an unconverted one test alike, so the gate saves
work and changes no answer a case could see.

  python spike/v53/plants.py            all plants (about two minutes each)
  python spike/v53/plants.py Q1 Q3      some
"""
import hashlib, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VM_DIR = os.path.join(ROOT, 'vm')
MAIN = os.path.join(VM_DIR, 'src', 'main.zig')
COMP = os.path.join(VM_DIR, 'src', 'compile.zig')
OUT = os.path.join(ROOT, 'runtime', 'v53', 'plant-build')
COURT = os.path.join(HERE, 'bound_court.py')
NL = chr(10)

PLANTS = [
    ('Q1', 'V01', 'a b name given an unproven call is not marked', COMP,
     [('        const want_bool = l == \'b\' and std.mem.eql(u8, op, "=") and self.unprovenCall(rhs);',
       '        const want_bool = false and l == \'b\' and std.mem.eql(u8, op, "=") and self.unprovenCall(rhs);')]),
    ('Q2', 'V02', 'the VM converts nothing', MAIN,
     [('                    if (v.tag == .int and (v.p.i == 0 or v.p.i == 1)) self.setRegB(base + in.a, Value.boolean(v.p.i == 1), false);',
       '                    if (false and v.tag == .int and (v.p.i == 0 or v.p.i == 1)) self.setRegB(base + in.a, Value.boolean(v.p.i == 1), false);')]),
    ('Q3', 'V02', 'a condition\'s value is not converted', COMP,
     [('        try self.boolExpr(n, t);' + NL + '        try out.append(self.scratch, try self.emit(.jfalsy, t, 0, if (hc) 1 else 0, 0));',
       '        try self.expr(n, t);' + NL + '        try out.append(self.scratch, try self.emit(.jfalsy, t, 0, if (hc) 1 else 0, 0));')]),
    ('Q4', 'V03', 'not\'s operand is not converted', COMP,
     [('            try self.boolExpr(n.namedChild(0), t);' + NL + '            _ = try self.emit(.lnot,',
       '            try self.expr(n.namedChild(0), t);' + NL + '            _ = try self.emit(.lnot,')]),
    ('Q5', 'V03', 'and/or\'s left operand is not converted', COMP,
     [('            try self.boolExpr(ln, t);', '            try self.expr(ln, t);')]),
    ('Q6', 'V03', 'and/or\'s right operand is not converted', COMP,
     [('            try self.boolExpr(rn, t2);', '            try self.expr(rn, t2);')]),
    ('Q7', 'V05', 'a method dispatched by name is proven Haro\'s', COMP,
     [('            if (self.isThis(callee.namedChild(0))) return false;' + NL + '            return true;',
       '            if (self.isThis(callee.namedChild(0))) return false;' + NL + '            return false;')]),
    ('Q8', 'V09', 'a function of a .haro file is unproven', COMP,
     [('            if (self.findFunc(name)) |f| return !self.haroNode(f.node);', '            if (self.findFunc(name)) |f| return f.node.isNull() or true;')]),
    ('Q9', 'V12', 'a built-in is unproven', COMP,
     [('                if (builtins.isBuiltin(low) or builtins.pascalOf(low) != null) return false;',
       '                if (false and (builtins.isBuiltin(low) or builtins.pascalOf(low) != null)) return false;')]),
    ('Q10', 'V13', 'a method reached through this is unproven', COMP,
     [('            if (self.isThis(callee.namedChild(0))) return false;' + NL + '            return true;',
       '            if (false and self.isThis(callee.namedChild(0))) return false;' + NL + '            return true;')]),
    ('Q11', 'V06', 'any integer is converted, 7 to false', MAIN,
     [('                    if (v.tag == .int and (v.p.i == 0 or v.p.i == 1)) self.setRegB(base + in.a, Value.boolean(v.p.i == 1), false);',
       '                    if (v.tag == .int) self.setRegB(base + in.a, Value.boolean(v.p.i == 1), false);')]),
]


def digest(b):
    return hashlib.sha256(b).hexdigest()


def main():
    want = set(sys.argv[1:])
    originals = {p: open(p, 'rb').read() for p in (MAIN, COMP)}

    def restore():
        for p, b in originals.items():
            open(p, 'wb').write(b)
            assert digest(open(p, 'rb').read()) == digest(b)

    results = []
    try:
        for pid, fixture, why, path, subs in PLANTS:
            if want and pid not in want:
                continue
            raw = originals[path].decode('utf-8')
            crlf = (chr(13) + NL) in raw
            text = raw.replace(chr(13) + NL, NL)
            stale = [o for o, _ in subs if text.count(o) != 1]
            if stale:
                print(f'{pid} STALE: {stale[0][:70]!r} ({text.count(stale[0])} found)', flush=True)
                results.append((pid, 'STALE'))
                continue
            planted = text
            for o, n in subs:
                planted = planted.replace(o, n)
            open(path, 'wb').write((planted.replace(NL, chr(13) + NL) if crlf else planted).encode('utf-8'))
            b = subprocess.run(['zig', 'build', '-Doptimize=ReleaseFast', '-j2', '-p', OUT], cwd=VM_DIR, capture_output=True, timeout=900)
            restore()
            if b.returncode != 0:
                print(f'{pid} BUILD FAILED: {b.stderr.decode("utf-8", "replace")[-400:]}', flush=True)
                results.append((pid, 'BUILD FAILED'))
                continue
            r = subprocess.run([sys.executable, COURT, '--vm', os.path.join(OUT, 'bin', 'haro.exe')], capture_output=True, timeout=900)
            out = r.stdout.decode('utf-8', 'replace')
            failed = re.findall(r'^  FAIL ([A-Z]\d+)', out, re.M)
            verdict = 'CAUGHT' if fixture in failed else 'MISSED'
            print(f'{pid} {verdict} ({why}): its fixture {fixture}; failed {", ".join(failed) or "none"}', flush=True)
            results.append((pid, verdict))
    finally:
        restore()
    caught = sum(1 for _, v in results if v == 'CAUGHT')
    print(f'PLANTS {caught} of {len(results)} caught')
    return 0 if caught == len(results) else 1


if __name__ == '__main__':
    sys.exit(main())
