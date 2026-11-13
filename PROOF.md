# Proof in Haro -- what the proving languages settled, and what Haro takes

**PROPOSED 2026-11-13, by the Haro desk, on the Principal's ask of that day: "further think this aspect in a profound manner by
analysing the reference lanaguges in the field ... the goal is to let Haro benefit from this aspect to be truley empowered as a
programming languge for governed agents and programs". Nothing here is ruled and nothing is built. Section 8 is the one row of
questions.**

Read for it: Haro at 903213a (CHARTER D51, D56, D61, D62; TYPES.md T7; SG1.md 7; PRINCIPLES.md 11); stzlib origin/main 2d3cb7cca,
`base/testoor/TESTOOR_EVIDENCE_LADDER.md`; the home pages of Lean, Rocq, Dafny and Cedar as they stood on 2026-11-13; the papers
named in section 9, from the desk's own reading.

---

## 0. The answer in eight sentences

1. The estate's first reading stands: proof is a grade of evidence a checker gives for exact source bytes, Testoor records it, and
   Haro's contracts are written in its closed condition language (the ladder; D61; D62).
2. The proving languages add one thing that reading did not have: **what is trusted must be small, and everything that searches is
   untrusted.** Lean and Rocq put a small kernel under every proof; whatever finds the proof -- a person, a tactic, a solver, a
   model -- is checked by it.
3. Haro already has that shape, one altitude up: **a model proposes, a court judges.** Haro's kernel is the court. Proof in Haro
   is the work of showing three things about it: nothing goes around it, nothing changes it, and it says what its declaration says.
4. For governed agents the theorem that matters is about **every action a declaration admits**, more than about one function's
   answer. Cedar, the policy language Amazon governs access and agents with, was designed so that such questions are decided by a
   solver; Haro's declared altitude is closed and total for the same reason and can be asked the same questions.
5. For programs, the rung that pays first is the one SPARK calls Silver: **no run-time error on any path**. Haro names every
   run-time refusal it has, so each one is an obligation that is either proved unreachable or stays a check.
6. A proof verdict in Haro has three named values and no fourth: **proved** (with a certificate), **refuted** (with the inputs
   that break it, kept as a fixture), **checked when it runs** (with the reason). A solver that runs out of time is the third.
7. Haro stays a programming language. It takes no dependent types into its surface, no tactic language and no proof assistant of
   its own; what a solver cannot settle is exported to one that exists, and its certificate recorded.
8. With models writing code and proofs, **the specification is where a wrong program gets in**. So a specification is checked for
   emptiness, a changed one is a class of change of its own, and a person's reading of it is a recorded fact.

## 1. What is already ruled

| ruled | where | state |
|---|---|---|
| the evidence ladder: named, observed, exemplified, generalised, exhausted, proved; a certificate is recorded, never checked, by Testoor; a stale hash counts as nothing | stzlib, TESTOOR-LADDER-01, the Principal 2026-11-08 | grades 0 to 4 built in Testoor |
| `haro check --facts`: per function, what the checker establishes, with the checker's commit and each file's sha256; a fact not established is absent | D61, v0.51 | built |
| `requires`, `ensures`, `invariant` in the closed, total condition language; checked when the program runs until a prover discharges them | D62, delegated | v0.70, then v0.71 |
| `uses [door]`, pure without it, the closure checked; `total`; `budget`; `personal` | D56, SG1.md 7 | ruled, not built |
| a sentence is a value only its court makes; text through a door is `unjudged` | D55, TYPES.md T7 | v0.69 |
| a language declares the doors its worlds may open (`NEEDS`, `OPENS`) | D51 | declared half built (v0.40) |
| a `.ring` file is outside every proof claim | HARO-PROOF-01 (e) | confirmed |

Open from that round: the proof profile's name (the Principal's), and the discharge path, which the desk read as "the closed
language straight to an SMT solver; general code later through the C target". This note settles the second and widens it.

## 2. The references, each read for what it settled

**Proof assistants on a kernel.**

| system | what it is | what it settled | what it costs |
|---|---|---|---|
| **Lean 4** | a functional language and proof assistant in one; a small kernel checks every proof; compiles to native code; its automation (`grind`, `bv_decide`, `omega`) is written in Lean and its results are re-checked by the kernel | the search for a proof needs no trust: its home page shows Google DeepMind's and Harmonic's models finding proofs the kernel then accepts, and it ships an interface meant for machines. AWS keeps an executable Lean model of Cedar beside the production code, proves properties of the model, and tests the two against each other on generated inputs; its page says no version ships unless model, proofs and tests are current | propositions are types: writing a specification is writing type theory. Every function the logic sees must be total |
| **Rocq** (formerly Coq), 9.2 | an interactive prover on a well-delimited kernel; programs are extracted to OCaml, Haskell or Scheme | whole artefacts can be proved: the CompCert C compiler, in which a 2011 random-testing study found no wrong-code defect in the proved passes; a checker for its own kernel (MetaRocq) | CompCert and seL4 (in Isabelle, about twenty person-years) are years of expert work each; proof scripts break when the code moves |

**Verification-aware languages on a solver.**

| system | what it is | what it settled | what it costs |
|---|---|---|---|
| **Dafny** | contracts and loop invariants in the language; obligations go to an SMT solver; compiles to C#, Java, JavaScript, Go, Python | a working programmer can prove real services; this is the form D62 chose | a large trusted base (the encoder and the solver); proofs that pass or time out as unrelated code changes (measured by Mariposa, FMCAD 2023) |
| **SPARK** (Ada) | a provable subset of Ada, through Why3 to several solvers | **adoption is a ladder**: Stone (the subset), Bronze (flow), Silver (no run-time error), Gold (key properties), Platinum (full correctness) -- and industry gets most of its value at Silver | each level above Silver costs markedly more per line |
| **Verus, F\*, Liquid Haskell, Why3** | Rust with proofs; a proof-oriented ML; refinement types; a shared intermediate with many provers | restricting what a specification may say (Liquid Haskell's decidable refinements; Verus's cautious quantifiers) buys predictable answers; several solvers behind one front (Why3) lowers the trust in any one | expressiveness given up on purpose |

**Languages analysed as a whole.**

| system | what it is | what it settled | what it costs |
|---|---|---|---|
| **Cedar** | an authorization policy language with no loops and no unbounded data, modelled and proved in Lean | **a governing language can be designed so that questions about every possible request are decided, with a counterexample when the answer is no**: "does this policy set ever allow what that one forbids", "is this rule ever reached". Amazon announced in December 2025 that its agent platform uses it to bound what an agent's tool calls may do | the language must stay small enough to stay decidable |
| **EverParse** | parsers and validators generated from a declared format, with a proof that each accepts exactly its format | **a judge generated from a declaration can be proved to say what the declaration says**; it guards network input in Windows | a verified generator is a research-grade artefact |
| **TLA+, Alloy, Ivy, the B method** | models of designs and of steps over time, checked inside a bound or proved inductive | most design defects show inside small bounds (Alloy); kept decidable, a failed invariant comes back as a concrete state (Ivy); refinement step by step, each with its obligations, built the Paris Metro's line 14 software (B) | a model is not the code |

**The work on agents.**

| work | what it settled |
|---|---|
| the reference monitor (Anderson, 1972) | a guard deserves trust when it is always invoked, cannot be tampered with, and is small enough to be verified. Every later system is an instance |
| enforceable security policies (Schneider, 2000) | a monitor that watches actions and refuses can enforce "this never happens"; it cannot enforce "this eventually happens" |
| proof-carrying code (Necula and Lee, 1996) | an untrusted producer ships its evidence with its code; the receiver runs a small checker and trusts nothing else |
| tracked capabilities for agents (Odersky and others, 2026) | an agent's code is typed by the capabilities it can reach; SG1.md 7 already takes it as `uses` |
| CaMeL (Google DeepMind, 2025) | prompt injection is stopped by design when text from outside can never choose control flow or a tool's argument; T7's `unjudged` is the same rule |
| guaranteed safe AI (Dalrymple, Bengio, Russell, Tegmark and others, 2024) | the three parts of a safety case for an AI system: a world model, a specification, a verifier |
| Clover (Stanford, 2023); the vericoding benchmark (2025) | code, contract and prose intent can be checked against each other; models asked to write proved code succeeded, as reported, on about 82% of Dafny tasks, 44% in Verus and 27% in Lean -- most where the automation is highest |

## 3. Eight lessons

**L1 -- Trust the checker, never the searcher.** Lean's and Rocq's kernels are small programs that only check; tactics,
solvers and models are outside them. Even Lean's bit-vector automation calls an outside SAT solver and re-checks its certificate.
*For Haro*: the court is the kernel. A solver's "proved" is a searcher's claim until a second, independent judge agrees.

**L2 -- Check the result, not the producer.** CompCert does not prove its register allocator; it proves a small validator of the
allocator's output. AWS does not prove Cedar's Rust code; it proves a model and compares the two on generated inputs. *For Haro*:
this is the court doctrine itself, and it says how to raise trust in a forged court without proving the forge: a second
implementation of the same declaration, and inputs generated from the grammar the forge already emits.

**L3 -- A specification language kept decidable gives answers.** Cedar, Ivy and Liquid Haskell always answer: yes, or no with an
example. Dafny, which lets a specification say anything, sometimes answers with a timeout that moves when unrelated code moves.
*For Haro*: "refuse loudly, and name what is refused" has no room for "unknown". The condition language is closed already; the
provable part of it is declared exactly (section 5.2), and a clause outside it is said to be outside.

**L4 -- The rung that pays is the absence of run-time errors.** SPARK's users stop mostly at Silver, where proof is nearly
automatic and removes a whole class of failure. *For Haro*: every run-time refusal is named -- TYPE_LETTER, KEY_TYPE,
INTEGER_OVERFLOW, DECIMAL_INEXACT, NO_FIELD, an index out of range, a maybe unresolved -- so "this function raises none of them" is
a finite list of obligations per function, with no specification to write.

**L5 -- To govern, analyse the policy over every action.** Proving an agent's code correct is the hard problem; bounding what any
code may do is the tractable one, and it is what Cedar, the reference monitor and the capability work all do. *For Haro*: a
declared language is a policy over sentences. The questions worth a proof are about all of its sentences at once.

**L6 -- Proof is cheap where the meaning is small.** Lean demands totality of what its logic sees. Dafny, Verus and Rust spend most
of their machinery on aliasing: who else can change this value. *For Haro*: the strict rungs were proof's groundwork -- a real
boolean, no coercion, exact integers that trap, exact decimals (a rational to a solver, where a float is bits), no null, one
spelling per name, and vectors, maps and records that are values, copied when assigned, so no second name changes them. `total`
and `uses` finish it.

**L7 -- With models writing proofs, the specification is the way in.** A model can satisfy `ensures true`, or a precondition
nothing meets, or change the contract with the code. Lean prints the axioms a proof rests on; Rocq lists what was admitted.
*For Haro*: no `assume`, no admitted clause; every contract checked for emptiness; a changed specification is its own class of
change; `spec_read_by` (Testoor's field) is a fact with a name in it.

**L8 -- A monitor enforces "never", not "eventually".** *For Haro*: the claim is exact -- within a declaration's bounds, nothing
refused is done. That an agent gets its task done is a matter for tests and for people.

## 4. What Haro does not take

- **Dependent types in the surface, and a tactic language.** They make the programmer a prover. Haro's contracts stay conditions.
- **A proof assistant of its own.** Two good ones exist, with their libraries and their models.
- **A specification language that can say anything.** What cannot be decided is said to be outside, and checked when it runs.
- **An escape hatch.** Nothing in a `.haro` file states a fact without evidence.
- **Trust in one solver.**

## 5. The design proposed

### 5.1 Haro generates reference monitors, and proof has three jobs

| the monitor must be | what shows it in Haro | kind of evidence | state |
|---|---|---|---|
| **always invoked**: no path to a door around the court | `uses` closed under calls and bounded by `NEEDS`; `unjudged` text never runs, never becomes a sentence unjudged, never directs a door; a handle second-class to its block; Harobanda's PID 1 holding the doors at the machine | proved by the checker on every path, as a type rule | ruled (D51, D56, T7); v0.69 and after |
| **tamper-proof**: the judged cannot change the judge | the closed world of the proof profile: no `eval`, no load at run time, no call the compiler cannot resolve; a court and its declaration named by their sha256 in every verdict | proved by the checker; hashes | profile ruled (D56); the hash is in `--facts` |
| **verifiable**: the court says what its declaration says | fixtures first, every protection planted, two builds and the same bytes -- and, proposed here, a second implementation compared on sentences generated from the forged grammar (5.5) | exemplified today; exhausted inside a bound, proposed | built; proposed |

Then two more jobs, for what runs inside the bounds: the policy itself is sound (5.4), and the program does what its contract says
(5.3).

### 5.2 Three verdicts, two judges, one limit that does not depend on the machine

- **The verdicts.** `proved` with a certificate; `refuted` with the inputs that break the clause, written as a fixture Testoor
  can keep as a tour; `checked when it runs`, with its reason -- outside the provable part, or the limit reached. Each is a row of
  `haro check --facts`.
- **The provable part**, declared exactly: booleans; integers and decimals with `+`, `-`, comparison, and multiplication by a
  literal; `Len`; a text's equality and length; membership in a list given; `all` and `some` over a list given or a declared
  range; a record's field, a map's `HasKey`. Floats, a product of two unknowns, and text patterns are outside, and said so.
- **Two judges.** A domain that is finite and small is **exhausted by the VM itself** -- no solver, the same answer on any
  machine -- and that is tried first. Otherwise the obligation is written as SMT-LIB text and given to **two solvers of different
  make**, which must agree; where one of them emits a proof, an independent checker re-checks it. A disagreement is a finding
  and the clause stays checked when it runs. This is D41's two builds, applied to the prover.
- **The solver is a program beside Haro, never part of it.** `haro` writes the obligation and reads the answer; a solver is found
  by name, and its name and version go into the certificate. The release carries no solver; the enumerator needs none.
- **The limit is a count of steps, never seconds.** This machine runs at 20 to 80% of its speed on some days; a proof that
  depends on the clock is the flaky test PX forbids.
- **The checked build keeps what was proved.** `haro` may leave out a check that was proved; its checked build keeps every one,
  and a proved clause that fails there raises PROOF_UNSOUND naming the certificate. Every run of the guard on both builds then
  tests the encoding against the VM, which is the gap no solver sees.

### 5.3 A function's levels, each a field of the facts

| level | what is established on every path | how | needs |
|---|---|---|---|
| **closed** | every call resolved; no text run as code; no load when running | the profile's refusals | D56 rung 1 |
| **contained** | reaches only the doors it names; no `unjudged` value runs or directs a door; no `personal` value leaves unguarded | the checker's closure and flow rules | T7, T9 |
| **bounded** | it ends, within a stated number of steps | `total` by construction; `budget` | T9 |
| **refusal-free** | none of Haro's named run-time refusals can be raised | one obligation per place a refusal could arise, judged as in 5.2 | the encoder |
| **contracted** | `requires`, `ensures`, `invariant` hold | the same judges; a callee is taken at its contract | D62, v0.70 and v0.71 |
| **proved elsewhere** | a property outside the provable part | exported (5.6); the certificate recorded | later |

The first three need no solver and are already ruled. A function may stand at any level; a floor (Testoor's) asks for one.

### 5.4 Asking a declaration about all of its sentences

A court judges one sentence. The same encoder, pointed at a declaration, answers for every sentence it admits. The questions
that govern an agent:

- **Reach**: can any sentence this language admits open door D? touch a seat marked PERSONAL without its SAFEGUARDS?
- **Refinement**: does the refined declaration admit only what its base's floor allows? what does version 2 admit that version 1
  refused -- answered with a sentence that shows it.
- **Health**: is a constraint never satisfiable (a dead rule), always satisfied (an empty rule), or do two rules contradict?
- **Sequence**, inside a bound: over every run of at most k moves from a declared start, does an invariant of the world hold?

A "no" comes with the sentence, or the run, that shows it. This needs only the declared altitude's meaning, which is closed and
total: no VM semantics enters the encoding. It is the smallest trusted base of anything proposed here, and it is what no
general-purpose language can offer, because their policies are code.

### 5.5 The court against its declaration

The forge emits a court and a grammar from one declaration, and the native court is a second implementation of judging. Proposed:
sentences generated from the grammar, and near-misses made from them by one change each, judged by both; any difference is a
finding with its sentence. Inside a declared bound on length this is grade 4, exhausted, for "the two courts agree".

### 5.6 What the solvers cannot settle

A function that is `total`, pure and closed is, with value semantics, a function in the mathematical sense. Such a function and its
contract can be written out as a definition and a theorem for a proof assistant. Lean 4 is the first candidate: one language for
the definition and the proof, native code to test the export against the VM, and the largest body of models trained to prove in
it. Haro checks nothing there: it records {checker, version, spec sha256, source sha256, verdict}, the shape D61 already fixed.

### 5.7 Rules for specifications

1. Every `requires` is shown satisfiable by a witness; every `ensures` is shown to refuse at least one answer. A clause that
   fails either is refused as EMPTY_CONTRACT.
2. No `.haro` construct asserts without evidence. A clause not proved is checked when it runs.
3. A change to a contract, a constraint or a floor is listed apart from a change to code in `--facts`, so a floor can say "an
   agent's change to a specification waits for a person".
4. The intent clause stays prose and is never compared by a machine that proves; a model may be asked whether intent, contract
   and code agree, and its answer is advice.

## 6. The order proposed

| rung | what | why here |
|---|---|---|
| v0.69 | judged types and `unjudged` (as planned) | the first half of "always invoked" |
| then | `uses` and `total` (T9), the proof profile's first refusals | completes "always invoked" and "bounded"; no solver |
| then | the encoder and the enumerator, with **5.4's questions on a declaration** as their first customer | smallest trusted base; what serves governed agents first |
| then | contracts written and checked when they run (D62's v0.70) | unchanged |
| then | discharge of contracts, and refusal-freedom (5.3) | the encoder's second customer; needs the VM's meaning encoded, tested by PROOF_UNSOUND |
| then | 5.5, the two courts compared on generated sentences | needs no rung above; can move earlier |
| later | 5.6, the export | when a property is met that the solvers leave open |

The one change to what was planned: the solver's first work is on declarations, before it is on functions.

## 7. What this costs, and where it stops

- The encoder is new trusted code. It is kept honest by the second solver, by the enumerator on small domains, and by the checked
  build.
- Nothing here proves a `.ring` file, a native, or what a door does once it is open.
- A proof is of a specification. Where a person is the last consumer -- a sound, a page, a sentence read -- CENTRAL-PERCEPTGATE-01
  holds unchanged.
- Sequence questions (5.4) are answered inside a bound. An unbounded proof needs an inductive invariant, which is 5.6's work.
- Two solvers are two programs a desk must have installed to produce grade 5 beyond what the enumerator reaches.

## 8. The questions, one row

HARO-PROOF-02, to the Principal, class: judgement except (e), which is naming --

- (a) the frame of section 5.1: Haro generates reference monitors, and proof's three jobs are those of the table;
- (b) the order of section 6: the solver's first customer is a declaration's questions (5.4), before a function's contracts;
- (c) section 5.2: three verdicts and no fourth; the solver a program beside Haro, two of different make; a step limit;
  PROOF_UNSOUND on the checked build;
- (d) section 5.6: an export to a proof assistant is in scope, later, as a recorded certificate only;
- (e) two names: the proof profile's (open since D62), and the word by which a declaration is asked 5.4's questions.

## 9. Read

Pages, 2026-11-13: lean-lang.org (home, learn, the Cedar use case); rocq-prover.org (home, about); dafny.org. Cedar's own site
served only its playground that day; what is said of Cedar is from its Lean use-case page and its paper.

Papers, from the desk's reading: Anderson, *Computer Security Technology Planning Study* (1972). Necula and Lee, *Safe Kernel
Extensions Without Run-Time Checking* (1996). Schneider, *Enforceable Security Policies* (2000). Leroy, *Formal Verification of a
Realistic Compiler* (2009); Rideau and Leroy on validating register allocation (2010); Yang and others, *Finding and Understanding
Bugs in C Compilers* (2011). Klein and others, *seL4: Formal Verification of an OS Kernel* (2009). Padon and others, *Ivy* (2016).
AdaCore and Thales, *Implementation Guidance for the Adoption of SPARK* (2017). Ramananandro and others, *EverParse* (2019). Zhou
and others, *Mariposa* (2023). Sun and others, *Clover* (2023). Cutler and others, *Cedar* (2024). Dalrymple and others, *Towards
Guaranteed Safe AI* (2024). Debenedetti and others, *Defeating Prompt Injections by Design* (2025). Odersky and others, *Tracking
Capabilities for Safer Agents* (2026). The vericoding benchmark's figures are as its authors reported them in 2025; the desk ran
none of it.
