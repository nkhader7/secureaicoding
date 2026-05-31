#!/usr/bin/env python3
"""
SAST Rule Format Comparison
Tests YAML vs TOML vs JSON vs Markdown as rule definition formats
for static application security testing (SAST).

Metrics:
  - Rules loadable (automated detection possible)
  - True positive rate  (TP / total TP fixtures)
  - False positive rate (FP / total TN fixtures)
  - Parse time          (median of 1000 iterations, microseconds)
  - File size           (bytes)
  - Feature matrix      (comments, multiline, anchors, schema, confidence)
  - Composite score     (weighted average of all dimensions)
"""

import json
import re
import time
import toml
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

BASE = Path(__file__).parent
FORMATS_DIR = BASE / "formats"
TP_DIR = BASE / "fixtures" / "true_positives"
TN_DIR = BASE / "fixtures" / "true_negatives"
BENCH_ITERATIONS = 1000

BAR_WIDTH = 30


# ─── Data structures ──────────────────────────────────────────────────────────

@dataclass
class Rule:
    id: str
    name: str
    severity: str
    pattern: Optional[str]


@dataclass
class Features:
    comments: bool
    multiline_strings: bool
    anchors_aliases: bool
    schema_validation: bool
    confidence_scoring: bool
    native_tooling: str       # descriptive string
    readability: int          # 1-5

    @property
    def score(self) -> int:
        """Feature richness score out of 100."""
        return (
            self.comments * 15
            + self.multiline_strings * 20
            + self.anchors_aliases * 20
            + self.schema_validation * 15
            + self.confidence_scoring * 15
            + self.readability * 3
        )


@dataclass
class FormatResult:
    name: str
    rules: list[Rule]
    parse_time_us: float
    file_size_bytes: int
    tp_hits: int
    tp_total: int
    fp_hits: int
    tn_total: int
    features: Features

    @property
    def tpr(self) -> float:
        return self.tp_hits / self.tp_total if self.tp_total else 0.0

    @property
    def fpr(self) -> float:
        return self.fp_hits / self.tn_total if self.tn_total else 0.0

    @property
    def composite_score(self) -> int:
        """
        Weighted composite (0–100):
          40% detection accuracy  (TPR — FPR penalty)
          25% feature richness
          20% maintainability     (comments + multiline)
          15% parse performance   (inverse, capped)
        """
        detection = max(0, self.tpr - self.fpr) * 40
        features = self.features.score * 0.25
        maintain = (self.features.comments + self.features.multiline_strings) * 10
        # parse score: 100% at <50μs, 0% at >500μs
        parse_score = max(0, 1 - (self.parse_time_us - 50) / 450) * 15
        return int(detection + features + maintain + parse_score)


# ─── Parsers ──────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> list[Rule]:
    with open(path) as f:
        data = yaml.safe_load(f)
    rules = []
    for r in data.get("rules", []):
        pattern = r.get("detection", {}).get("regex_pattern") or r.get("pattern")
        rules.append(Rule(r["id"], r["name"], r["severity"], pattern))
    return rules


def load_toml(path: Path) -> list[Rule]:
    with open(path) as f:
        data = toml.load(f)
    rules = []
    for r in data.get("rules", []):
        # TOML uses flat schema: confidence is scalar fields, not nested arrays.
        # This is a structural limitation vs YAML's anchor-based weighted arrays.
        rules.append(Rule(r["id"], r["name"], r["severity"], r.get("pattern")))
    return rules


def load_json(path: Path) -> list[Rule]:
    with open(path) as f:
        data = json.load(f)
    rules = []
    for r in data.get("rules", []):
        pattern = r.get("detection", {}).get("regex_pattern") or r.get("pattern")
        rules.append(Rule(r["id"], r["name"], r["severity"], pattern))
    return rules


def load_markdown(_path: Path) -> list[Rule]:
    # Markdown has no machine-readable patterns — returns empty list.
    return []


LOADERS = {
    "YAML": (FORMATS_DIR / "sast_rules.yaml", load_yaml),
    "TOML": (FORMATS_DIR / "sast_rules.toml", load_toml),
    "JSON": (FORMATS_DIR / "sast_rules.json", load_json),
    "Markdown": (FORMATS_DIR / "sast_rules.md", load_markdown),
}

FEATURE_MAP = {
    "YAML": Features(
        comments=True,
        multiline_strings=True,
        anchors_aliases=True,
        schema_validation=True,
        confidence_scoring=True,
        native_tooling="Rich (Semgrep, ansible-lint, schema validators)",
        readability=4,
    ),
    "TOML": Features(
        comments=True,
        multiline_strings=True,
        anchors_aliases=False,
        schema_validation=False,
        confidence_scoring=True,
        native_tooling="Good (taplo, cargo, toml-sort)",
        readability=3,
    ),
    "JSON": Features(
        comments=False,
        multiline_strings=False,
        anchors_aliases=False,
        schema_validation=True,
        confidence_scoring=True,
        native_tooling="Rich (JSON Schema, jq, most languages built-in)",
        readability=2,
    ),
    "Markdown": Features(
        comments=True,
        multiline_strings=True,
        anchors_aliases=False,
        schema_validation=False,
        confidence_scoring=False,
        native_tooling="Basic (renderers, linters, no rule extraction)",
        readability=5,
    ),
}


# ─── Detection engine ─────────────────────────────────────────────────────────

def scan_file(content: str, rules: list[Rule]) -> list[str]:
    """Return list of rule IDs that matched."""
    hits = []
    for rule in rules:
        if rule.pattern and re.search(rule.pattern, content, re.MULTILINE):
            hits.append(rule.id)
    return hits


def run_format(name: str) -> FormatResult:
    path, loader = LOADERS[name]

    # ── Benchmark parse time (median of BENCH_ITERATIONS) ──────────────────
    times = []
    for _ in range(BENCH_ITERATIONS):
        t0 = time.perf_counter()
        loader(path)
        times.append((time.perf_counter() - t0) * 1e6)
    times.sort()
    parse_us = times[BENCH_ITERATIONS // 2]

    rules = loader(path)
    size = path.stat().st_size

    # ── Scan true-positive fixtures ─────────────────────────────────────────
    tp_files = sorted(TP_DIR.iterdir())
    tp_hits = 0
    for f in tp_files:
        content = f.read_text()
        if scan_file(content, rules):
            tp_hits += 1

    # ── Scan true-negative fixtures ─────────────────────────────────────────
    tn_files = sorted(TN_DIR.iterdir())
    fp_hits = 0
    for f in tn_files:
        content = f.read_text()
        if scan_file(content, rules):
            fp_hits += 1

    return FormatResult(
        name=name,
        rules=rules,
        parse_time_us=parse_us,
        file_size_bytes=size,
        tp_hits=tp_hits,
        tp_total=len(tp_files),
        fp_hits=fp_hits,
        tn_total=len(tn_files),
        features=FEATURE_MAP[name],
    )


# ─── Graph helpers ────────────────────────────────────────────────────────────

def bar(value: float, max_value: float, width: int = BAR_WIDTH) -> str:
    if max_value == 0:
        return "░" * width
    filled = int(round((value / max_value) * width))
    filled = min(filled, width)
    return "█" * filled + "░" * (width - filled)


def pct(v: float) -> str:
    return f"{v * 100:.1f}%"


def yn(v: bool) -> str:
    return "✅" if v else "❌"


def stars(n: int) -> str:
    return "★" * n + "☆" * (5 - n)


# ─── Report ───────────────────────────────────────────────────────────────────

def print_report(results: list[FormatResult]) -> None:
    W = 72
    SEP = "═" * W

    print()
    print(SEP)
    print("  SAST Rule Format Comparison — YAML vs TOML vs JSON vs Markdown")
    print(f"  Rules tested: 5 | Fixtures: {results[0].tp_total} TP + {results[0].tn_total} TN | "
          f"Benchmark: {BENCH_ITERATIONS} iterations")
    print(SEP)

    # ── Summary table ──────────────────────────────────────────────────────
    col = 12
    hdr = f"{'Metric':<28}" + "".join(f"{r.name:>{col}}" for r in results)
    print()
    print(hdr)
    print("─" * W)

    rows = [
        ("Rules loaded",      [str(len(r.rules))            for r in results]),
        ("True positives",    [f"{r.tp_hits}/{r.tp_total}"  for r in results]),
        ("False positives",   [f"{r.fp_hits}/{r.tn_total}"  for r in results]),
        ("TP rate",           [pct(r.tpr)                   for r in results]),
        ("FP rate",           [pct(r.fpr)                   for r in results]),
        ("Parse time (μs)",   [f"{r.parse_time_us:.0f}"     for r in results]),
        ("File size (bytes)", [f"{r.file_size_bytes:,}"     for r in results]),
    ]
    for label, vals in rows:
        print(f"  {label:<26}" + "".join(f"{v:>{col}}" for v in vals))

    print("─" * W)
    feature_rows = [
        ("Comments",          [yn(r.features.comments)           for r in results]),
        ("Multi-line strings",[yn(r.features.multiline_strings)  for r in results]),
        ("Anchors/aliases",   [yn(r.features.anchors_aliases)    for r in results]),
        ("Schema validation", [yn(r.features.schema_validation)  for r in results]),
        ("Confidence scoring",[yn(r.features.confidence_scoring) for r in results]),
        ("Readability",       [stars(r.features.readability)     for r in results]),
    ]
    for label, vals in feature_rows:
        print(f"  {label:<26}" + "".join(f"{v:>{col}}" for v in vals))

    print("─" * W)
    print(f"  {'Composite score (0–100)':<26}" +
          "".join(f"{r.composite_score:>{col}}" for r in results))
    print()

    # ── Bar graphs ─────────────────────────────────────────────────────────
    sections = [
        (
            "Detection Rate (True Positive Rate)  — higher is better",
            [(r.name, r.tpr, 1.0, pct(r.tpr)) for r in results],
        ),
        (
            "False Positive Rate  — lower is better",
            [(r.name, r.fpr, 1.0, pct(r.fpr) if r.rules else "N/A (no rules)") for r in results],
        ),
        (
            "Parse Time (μs, median of 1 000 iterations)  — lower is better",
            [(r.name, r.parse_time_us, max(r2.parse_time_us for r2 in results) * 1.1,
              f"{r.parse_time_us:.0f}μs") for r in results],
        ),
        (
            "File Size (bytes)  — context for maintainability",
            [(r.name, r.file_size_bytes, max(r2.file_size_bytes for r2 in results) * 1.1,
              f"{r.file_size_bytes:,}B") for r in results],
        ),
        (
            "Composite Score (0–100)  — weighted: detection 40%, features 25%, "
            "maintainability 20%, perf 15%",
            [(r.name, r.composite_score, 100, f"{r.composite_score}/100") for r in results],
        ),
    ]

    for title, entries in sections:
        print(f"  {title}")
        print("  " + "─" * (W - 2))
        for name, value, max_val, label in entries:
            b = bar(value, max_val)
            print(f"  {name:<10}  {b}  {label}")
        print()

    # ── Feature matrix ─────────────────────────────────────────────────────
    print("  Feature Matrix")
    print("  " + "─" * (W - 2))
    feat_labels = [
        ("Comments in rule files", lambda r: yn(r.features.comments)),
        ("Multi-line pattern strings", lambda r: yn(r.features.multiline_strings)),
        ("Anchors/aliases (DRY shared patterns)", lambda r: yn(r.features.anchors_aliases)),
        ("Schema validation tooling", lambda r: yn(r.features.schema_validation)),
        ("Confidence scoring support", lambda r: yn(r.features.confidence_scoring)),
        ("Readability (1–5 ★)", lambda r: stars(r.features.readability)),
        ("Tooling ecosystem", lambda r: r.features.native_tooling.split("(")[0].strip()),
    ]
    for label, fn in feat_labels:
        print(f"  {label:<40}", end="")
        for r in results:
            print(f"  {fn(r):<14}", end="")
        print()
    print()

    # ── Verdict ────────────────────────────────────────────────────────────
    winner = max(results, key=lambda r: r.composite_score)
    print(SEP)
    print("  Verdict")
    print("─" * W)
    verdicts = {
        "YAML": (
            "Best overall for security rule authoring. Block scalars make regex readable, "
            "anchors eliminate repetition, and the ecosystem (Semgrep, schema validators) "
            "is widest. Recommended default."
        ),
        "TOML": (
            "Strong alternative. Literal strings (''') store regex cleanly without double-escape. "
            "Slightly more verbose for nested confidence structures. No anchors means shared "
            "patterns must be duplicated. Good for teams already using TOML (Rust/Cargo projects)."
        ),
        "JSON": (
            "Avoid for hand-authored rules. Double-escaped regex (\\\\s, \\\\b) is error-prone, "
            "no comments mean patterns are undocumented, and nested structures are verbose. "
            "Suitable as a machine-generated interchange format only."
        ),
        "Markdown": (
            "Zero automated detection — no machine-readable patterns. Ideal as human-facing "
            "documentation alongside a structured format. Markdown-only rules require a human "
            "reviewer per file, which does not scale. Use as reference, not as the rule source."
        ),
    }
    for r in results:
        marker = " ◀ WINNER" if r.name == winner.name else ""
        print(f"\n  {r.name}{marker} (score {r.composite_score}/100)")
        print(f"  {verdicts[r.name]}")

    print()
    print(SEP)


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    results = [run_format(name) for name in ("YAML", "TOML", "JSON", "Markdown")]
    print_report(results)
