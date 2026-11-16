#!/usr/bin/env python3
"""Token-level preservation check for an academic edit.

Compares an original and a revised manuscript and reports differences in what an editing pass must
not change. Two tiers:

  FAIL   must match exactly: citation keys, math spans, numbers, number+unit quantities, "label =
         value" statistics, comparison operators, URLs, source comments, LaTeX structure (labels,
         refs, environments, includes, macro definitions, bibliography), locked declaration
         sections, and --protect terms.
  CHECK  shown for human review: number words, direction words (up/down), number order, citation
         grouping per sentence, and hedge / negation / causal / association / scope wording.

Standard library only. Reads the files named on the command line and writes a Markdown report to
stdout. It makes no network access and opens no other files.

    python3 scripts/preservation_check.py ORIGINAL REVISED [--protect TERMS.txt] [--accept TOKEN ...]

  --protect FILE   one term per line (e.g. a glossary of multi-word technical terms); each must
                   occur the same number of times in both files.
  --accept TOKEN   an intended difference, spelled exactly as this report prints it (e.g.
                   --accept "17 years"). A matching FAIL difference
                   is listed as ACCEPTED instead of failing. Every accepted token must be named and
                   explained in the change report.

Exit status: 0 = no FAIL differences, 1 = FAIL differences, 2 = usage error.
A clean result does NOT prove meaning was preserved. It narrows where the semantic review must look.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

MINUS = "\u2212"
SUPERSCRIPT_DIGITS = str.maketrans("\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079",
                                   "0123456789")

# ---------------------------------------------------------------- citations
_AUTH = r"[A-Z][A-Za-z'\-]+(?: et al\.| (?:and|&) [A-Z][A-Za-z'\-]+)?"
_AY = _AUTH + r",? \d{4}[a-z]?"
CITE_PATTERNS = [
    (re.compile(r"\\(?:[a-zA-Z]*cite[a-zA-Z]*)\*?(?:\[[^\]]*\])*\{([^}]*)\}"), "latex"),
    (re.compile(r"\[(\d+(?:\s*[-\u2013,]\s*\d+)*)\]"), "numeric"),
    (re.compile(r"\[(@[^\]]+)\]"), "pandoc"),
    (re.compile(r"\[\^([^\]]+)\]"), "footnote"),
    (re.compile(r"([\u00b9\u00b2\u00b3\u2070\u2074-\u2079]+)"), "superscript"),
    (re.compile(r"\((?:(?:cf\.|e\.g\.,?|see|see also) )?(" + _AY + r"(?:; ?" + _AY + r")*)\)"),
     "author-year"),
    (re.compile(r"\b(" + _AUTH + r") \((\d{4}[a-z]?)\)"), "narrative"),
]

# ---------------------------------------------------------------- math / latex
MATH_PATTERNS = [
    re.compile(r"\\begin\{(equation|align|gather|multline|eqnarray)(\*?)\}(.+?)\\end\{\1\2\}", re.S),
    re.compile(r"\$\$(.+?)\$\$", re.S),
    re.compile(r"\\\[(.+?)\\\]", re.S),
    re.compile(r"(?<![\\$])\$(?!\$)(.+?)(?<![\\$])\$(?!\$)", re.S),
]
LATEX_STRUCT = {
    "labels": re.compile(r"\\label\{([^}]*)\}"),
    "refs": re.compile(r"\\(?:ref|eqref|autoref|cref|Cref|pageref|nameref)\{([^}]*)\}"),
    "environments": re.compile(r"\\begin\{([^}]*)\}"),
    "includes": re.compile(r"\\(?:input|include|includegraphics|bibliography|addbibresource)"
                           r"(?:\[[^\]]*\])?\{([^}]*)\}"),
    "macro definitions": re.compile(r"\\(?:newcommand|renewcommand|providecommand|DeclareMathOperator)"
                                    r"\*?\{?(\\[A-Za-z@]+)|\\def(\\[A-Za-z@]+)"),
}
BIB_BLOCK = re.compile(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", re.S)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
TEX_COMMENT = re.compile(r"(?<!\\)%[^\n]*")
LOOKS_LATEX = re.compile(r"\\(?:documentclass|begin|section|subsection|cite[a-z]*|usepackage)\b")

# ---------------------------------------------------------------- numbers
URL_RE = re.compile(r"https?://[^\s)>\]]+")
NUM_RE = re.compile(r"(?<![\w.])[-\u2212]?\d+(?:[.,]\d+)*(?:\s?%)?")
UNITS = (r"%|percent|percentage points?|points?|pp|mg|mcg|µg|μg|ng|g|kg|mL|ml|L|µL|mmol|mol|mM|µM|nM|"
         r"mm|cm|m|km|µm|nm|m²|m2|km²|ha|h|hr|hrs|hours?|min|minutes?|s|sec|seconds?|ms|days?|weeks?|"
         r"months?|years?|yr|°C|°F|K|NTU|Hz|kHz|MHz|GHz|W|kW|V|mV|A|mA|GB|MB|TB|KB|bits?|bytes?|"
         r"FLOPs?|params?|tokens?|epochs?|seeds?|x|×|fold|mmHg|bpm|IU|U|mL/min(?:/1\.73 ?m²)?")
QTY_RE = re.compile(r"(?<![\w.])([-\u2212]?\d+(?:[.,]\d+)*)\s?-?(" + UNITS + r")(?![A-Za-z])")
STAT_RE = re.compile(r"\b(?:p|n|N|r|R\^?2|t|F|z|d|OR|RR|HR|AUC|AUROC|CI|SD|SE|SEM|df|beta|β)"
                     r"\s*[=<>≤≥]\s*[-\u2212]?[\d.]+")
OPERATOR_RE = re.compile(r"[=<>≤≥±×≈≠]|\\pm|\\leq?|\\geq?|\\times|\\approx|\\neq")

# ---------------------------------------------------------------- wording (CHECK tier)
NUMBER_WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                "eleven", "twelve", "twenty", "dozen", "hundred", "thousand", "million", "billion",
                "first", "second", "third", "fourth", "fifth", "half", "twice", "double", "triple",
                "single", "both", "several", "most", "majority", "minority"]
DIRECTION = {
    "up": r"increas\w*|rais\w*|rise[sn]?|rising|rose|higher|greater|more|improv\w*|gain\w*|"
          r"exceed\w*|grow\w*|grew|boost\w*|enhanc\w*|outperform\w*|above",
    "down": r"decreas\w*|reduc\w*|lower\w*|fewer|less|declin\w*|drop\w*|fell|fall\w*|worse\w*|"
            r"shrink\w*|shrank|diminish\w*|degrad\w*|underperform\w*|below",
}
WATCH = {
    "hedge": ["may", "might", "could", "suggest", "suggests", "suggesting", "possible", "possibly",
              "likely", "appear", "appears", "consistent with", "preliminary", "potential",
              "perhaps", "approximately", "about"],
    "negation": ["not", "no", "none", "neither", "nor", "without", "did not", "does not", "cannot",
                 "need not"],
    "modality": ["must", "should", "will", "would", "can", "need", "required", "only where",
                 "only if", "unless", "if"],
    "causal/strong": ["cause", "causes", "caused", "causal", "prove", "proves", "demonstrate",
                      "demonstrates", "establish", "establishes", "confirm", "confirms", "leads to",
                      "results in", "due to", "because", "therefore", "thus"],
    "association": ["associated", "association", "correlated", "correlation", "linked", "related"],
    "scope": ["all", "always", "never", "every", "universal", "universally", "generalize", "only",
              "first", "any", "in general"],
    "tense (planned vs done)": ["will", "we will", "have added", "we added", "we have", "planned",
                                "future"],
}
DECLARATION_HEAD = re.compile(
    r"(?im)^(?:#{1,6}\s*|\\(?:section|subsection|paragraph)\*?\{)\s*"
    r"((?:declaration of )?(?:ai|generative ai|artificial intelligence)[^\n}]*|data availability[^\n}]*|"
    r"code availability[^\n}]*|conflicts? of interest[^\n}]*|competing interests?[^\n}]*|"
    r"funding[^\n}]*|author contributions[^\n}]*|credit[^\n}]*|ethics[^\n}]*|"
    r"acknowledg(?:e)?ments?[^\n}]*)\}?\s*$")
ANY_HEAD = re.compile(r"(?m)^(?:#{1,6}\s|\\(?:section|subsection|chapter)\*?\{)")
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(\[\\])")


def expand_numeric(group: str) -> list[str]:
    keys: list[str] = []
    for part in re.split(r"\s*,\s*", group):
        m = re.fullmatch(r"(\d+)\s*[-\u2013]\s*(\d+)", part)
        if m and 0 <= int(m.group(2)) - int(m.group(1)) < 200:
            keys.extend(str(i) for i in range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.strip():
            keys.append(part.strip())
    return keys


def citations(text: str) -> tuple[Counter, str]:
    keys: Counter = Counter()
    for pat, kind in CITE_PATTERNS:
        for m in pat.finditer(text):
            g = m.group(1)
            if kind == "latex":
                keys.update(k.strip() for k in g.split(",") if k.strip())
            elif kind == "numeric":
                keys.update(f"[{k}]" for k in expand_numeric(g))
            elif kind == "pandoc":
                keys.update(k.strip().lstrip("@") for k in g.split(";") if k.strip())
            elif kind == "footnote":
                keys[f"[^{g}]"] += 1
            elif kind == "superscript":
                keys[f"note {g.translate(SUPERSCRIPT_DIGITS)}"] += 1
            elif kind == "narrative":
                keys[f"{m.group(1)}, {m.group(2)}"] += 1
            else:
                keys.update(k.strip() for k in g.split(";") if k.strip())
        text = pat.sub(" ", text)
    return keys, text


def extract(pats, text: str) -> tuple[Counter, str]:
    found: Counter = Counter()
    for pat in pats:
        for m in pat.finditer(text):
            found[re.sub(r"\s+", " ", m.group(0)).strip()] += 1
        text = pat.sub(" ", text)
    return found, text


def norm_num(tok: str) -> str:
    return tok.replace(MINUS, "-").replace(" ", "")


def latex_struct(text: str) -> dict[str, Counter]:
    out = {}
    for name, pat in LATEX_STRUCT.items():
        c: Counter = Counter()
        for m in pat.finditer(text):
            for g in m.groups():
                if g:
                    c.update(k.strip() for k in g.split(",") if k.strip())
        out[name] = c
    out["bibliography block"] = Counter(re.sub(r"\s+", " ", b) for b in BIB_BLOCK.findall(text))
    return out


def declarations(text: str) -> Counter:
    c: Counter = Counter()
    for m in DECLARATION_HEAD.finditer(text):
        start = m.end()
        nxt = ANY_HEAD.search(text, start)
        body = text[start:nxt.start() if nxt else len(text)]
        c[f"{m.group(1).strip()}: {re.sub(r'\s+', ' ', body).strip()}"] += 1
    return c


def words(text: str, vocab: list[str]) -> Counter:
    low = text.lower()
    c: Counter = Counter()
    for w in vocab:
        n = len(re.findall(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low))
        if n:
            c[w] = n
    return c


def direction(text: str) -> Counter:
    low = text.lower()
    return Counter({k: len(re.findall(r"\b(?:" + v + r")\b", low)) for k, v in DIRECTION.items()})


def sentence_cites(text: str) -> list[tuple[frozenset, str]]:
    out = []
    for sent in SENT_SPLIT.split(re.sub(r"\s+", " ", text)):
        keys, _ = citations(sent)
        if keys:
            out.append((frozenset(keys), sent.strip()))
    return out


def fmt(c: Counter) -> str:
    return ", ".join(f"`{k}`" + (f" x{v}" if v > 1 else "") for k, v in sorted(c.items())) or "none"


class Report:
    def __init__(self, accept: list[str]):
        self.accept = set(accept)
        self.used_accept: set[str] = set()
        self.fails = 0
        self.lines: list[str] = []

    def fail_section(self, label: str, a: Counter, b: Counter, show_counts: bool = True) -> None:
        missing, added = a - b, b - a
        acc_m = Counter({k: v for k, v in missing.items() if k in self.accept})
        acc_a = Counter({k: v for k, v in added.items() if k in self.accept})
        self.used_accept |= set(acc_m) | set(acc_a)
        missing, added = missing - acc_m, added - acc_a
        if not a and not b:
            return
        status = "OK" if not missing and not added else "FAIL"
        if acc_m or acc_a:
            status += " (with accepted differences)"
        self.fails += not (status.startswith("OK"))
        self.lines.append(f"### {label}: {status}\n")
        if show_counts:
            self.lines.append(f"- count: {sum(a.values())} -> {sum(b.values())}")
        self.lines.append(f"- missing in revised: {fmt(missing)}")
        self.lines.append(f"- added in revised: {fmt(added)}")
        if acc_m or acc_a:
            self.lines.append(f"- ACCEPTED (must be explained in the report): {fmt(acc_m + acc_a)}")
        self.lines.append("")


def run(orig: str, rev: str, protect: list[str], accept: list[str]) -> tuple[str, int]:
    R = Report(accept)
    comment_pats = [HTML_COMMENT] + ([TEX_COMMENT] if LOOKS_LATEX.search(orig) else [])
    o_com, o_rest = extract(comment_pats, orig)
    r_com, r_rest = extract(comment_pats, rev)
    o_struct, r_struct = latex_struct(o_rest), latex_struct(r_rest)
    o_cite, o_rest = citations(o_rest)
    r_cite, r_rest = citations(r_rest)
    o_math, o_rest = extract(MATH_PATTERNS, o_rest)
    r_math, r_rest = extract(MATH_PATTERNS, r_rest)
    o_url, o_rest = extract([URL_RE], o_rest)
    r_url, r_rest = extract([URL_RE], r_rest)
    for k in ("labels", "refs", "includes"):  # strip so their contents aren't counted as numbers
        o_rest, r_rest = LATEX_STRUCT[k].sub(" ", o_rest), LATEX_STRUCT[k].sub(" ", r_rest)

    def toks(rx, s, n=True):
        return Counter(norm_num(re.sub(r"\s+", " ", t if isinstance(t, str) else " ".join(t)))
                       for t in rx.findall(s)) if n else Counter(rx.findall(s))

    o_qty = Counter(f"{norm_num(n)} {u}" for n, u in QTY_RE.findall(o_rest))
    r_qty = Counter(f"{norm_num(n)} {u}" for n, u in QTY_RE.findall(r_rest))

    R.lines.append("## FAIL tier (must match)\n")
    R.fail_section("Citation keys", o_cite, r_cite)
    R.fail_section("Math spans", o_math, r_math)
    R.fail_section("Statistics (label = value)",
                   Counter(re.sub(r"\s+", "", norm_num(s)) for s in STAT_RE.findall(o_rest)),
                   Counter(re.sub(r"\s+", "", norm_num(s)) for s in STAT_RE.findall(r_rest)))
    R.fail_section("Numbers", toks(NUM_RE, o_rest), toks(NUM_RE, r_rest))
    R.fail_section("Quantities (number + unit)", o_qty, r_qty)
    R.fail_section("Comparison operators", Counter(OPERATOR_RE.findall(o_rest)),
                   Counter(OPERATOR_RE.findall(r_rest)))
    R.fail_section("URLs", o_url, r_url)
    R.fail_section("Source comments (kept verbatim; may contain text addressed to an AI)", o_com, r_com)
    for name in o_struct:
        R.fail_section(f"LaTeX {name}", o_struct[name], r_struct[name])
    R.fail_section("Locked declaration sections (AI use, data availability, funding, ethics, ...)",
                   declarations(orig), declarations(rev), show_counts=False)
    if protect:
        R.fail_section("Protected terms (--protect)", words(orig, protect), words(rev, protect))
    if R.fails == 0:
        R.lines.append("No FAIL-tier differences.\n")

    R.lines.append("## CHECK tier (review each change; not errors by themselves)\n")
    o_groups = sentence_cites(orig)
    r_groups = {k for k, _ in sentence_cites(rev)}
    moved = [(k, s) for k, s in o_groups if k not in r_groups]
    if moved:
        R.lines.append("**Citation groups no longer together in one sentence:**\n")
        for k, s in moved:
            R.lines.append(f"- {fmt(Counter(k))}: \"{s[:160]}{'...' if len(s) > 160 else ''}\"")
        R.lines.append("")
    else:
        R.lines.append("- Citation grouping: every original citation group still sits in one sentence.")
    on, rn = [norm_num(n) for n in NUM_RE.findall(o_rest)], [norm_num(n) for n in NUM_RE.findall(r_rest)]
    if Counter(on) == Counter(rn) and on != rn:
        R.lines.append("- Number order: same numbers, different order. Check that none moved to another quantity.")
    od, rd = direction(orig), direction(rev)
    R.lines.append(f"- Direction words: up {od['up']}->{rd['up']}, down {od['down']}->{rd['down']}"
                   + ("" if od == rd else "  <- check no effect changed direction"))
    nw_o, nw_r = words(orig, NUMBER_WORDS), words(rev, NUMBER_WORDS)
    ch = [f"`{w}` {nw_o[w]}->{nw_r[w]}" for w in sorted(set(nw_o) | set(nw_r)) if nw_o[w] != nw_r[w]]
    R.lines.append(f"- Number words: {', '.join(ch) if ch else 'no change'}")
    for cat, vocab in WATCH.items():
        ow, rw = words(orig, vocab), words(rev, vocab)
        ch = [f"`{w}` {ow[w]}->{rw[w]}" for w in sorted(set(ow) | set(rw)) if ow[w] != rw[w]]
        R.lines.append(f"- {cat}: {', '.join(ch) if ch else 'no change'}")
    unused = R.accept - R.used_accept
    if unused:
        R.lines.append(f"- Unused --accept tokens (no matching difference): {fmt(Counter(unused))}")
    R.lines.append("")
    R.lines.append(f"**FAIL-tier sections differing: {R.fails}.** A clean result does not prove meaning "
                   "was preserved. Still do the semantic reread: a number attached to a different "
                   "quantity, a citation now supporting a different claim, a moved qualifier, reversed "
                   "cause and effect, planned work stated as done.")
    return "\n".join(R.lines), (1 if R.fails else 0)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original")
    ap.add_argument("revised")
    ap.add_argument("--protect", help="file with one protected term per line")
    ap.add_argument("--accept", action="append", default=[], help="intended difference token")
    a = ap.parse_args(argv)
    orig = open(a.original, encoding="utf-8").read()
    rev = open(a.revised, encoding="utf-8").read()
    protect = []
    if a.protect:
        protect = [t.strip().lower() for t in open(a.protect, encoding="utf-8") if t.strip()
                   and not t.startswith("#")]
    body, code = run(orig, rev, protect, a.accept)
    print(f"# Preservation check\n\nOriginal: `{a.original}`  \nRevised: `{a.revised}`\n")
    print(body)
    return code


if __name__ == "__main__":
    sys.exit(main())
