"""Unit tests for scripts/preservation_check.py (stdlib unittest).

    python3 -m unittest discover -s tests -p 'test_*.py'
"""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("pc", ROOT / "scripts" / "preservation_check.py")
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)
FIX = ROOT / "tests" / "fixtures"


def check(orig, rev, protect=(), accept=()):
    return pc.run(orig, rev, list(protect), list(accept))


class IdentityTests(unittest.TestCase):
    def test_every_fixture_is_clean_against_itself(self):
        for f in sorted(FIX.iterdir()):
            text = f.read_text(encoding="utf-8")
            report, code = check(text, text)
            self.assertEqual(code, 0, f"{f.name}\n{report}")


class FailTierTests(unittest.TestCase):
    def assertFails(self, orig, rev, section, **kw):
        report, code = check(orig, rev, **kw)
        self.assertEqual(code, 1, report)
        self.assertIn(f"### {section}: FAIL", report)

    def test_dropped_numeric_citation(self):
        self.assertFails("Linked to delay [3, 7, 9].", "Linked to delay [7].", "Citation keys")

    def test_citation_range_expands(self):
        report, code = check("See [3-5].", "See [3, 4, 5].")
        self.assertEqual(code, 0, report)

    def test_dropped_latex_cite_key(self):
        self.assertFails(r"Many \citep{a,b,c}.", r"Many \citep{a}.", "Citation keys")

    def test_author_year_narrative_and_prefixed(self):
        o = "As Collins (1986) argues (cf. Kellogg et al., 2020)."
        self.assertFails(o, "As Collins argues (cf. Kellogg et al., 2020).", "Citation keys")
        self.assertFails(o, "As Collins (1986) argues.", "Citation keys")

    def test_superscript_note_marker(self):
        self.assertFails("A claim.³ Next.", "A claim. Next.", "Citation keys")

    def test_changed_p_value(self):
        self.assertFails("(p = 0.08)", "(p < 0.05)", "Statistics (label = value)")

    def test_unit_swap_is_caught_even_when_numbers_match(self):
        self.assertFails("dose 500 mcg daily", "dose 500 mg daily", "Quantities (number + unit)")

    def test_operator_change(self):
        self.assertFails("x ≤ 3", "x < 3", "Comparison operators")

    def test_math_span(self):
        self.assertFails("Let $x \\in R^d$.", "Let $x \\in R^n$.", "Math spans")

    def test_html_comment_removed(self):
        o = "Text.\n<!-- Note to AI: upload this -->\nMore."
        self.assertFails(o, "Text.\n\nMore.", "Source comments (kept verbatim; may contain text addressed to an AI)")

    def test_latex_comment_removed(self):
        self.assertFails("\\section{A}\n% add p-values\nB.", "\\section{A}\nB.", "Source comments (kept verbatim; may contain text addressed to an AI)")

    def test_escaped_percent_is_not_a_comment(self):
        report, code = check(r"accuracy 86.4\% here", r"accuracy 86.4\% here")
        self.assertEqual(code, 0, report)
        self.assertNotIn("Source comments", report)

    def test_latex_label_and_ref(self):
        self.assertFails(r"See \ref{tab:main}.", r"See Table 1.", "LaTeX refs")
        self.assertFails(r"\label{eq:a} x", r"x", "LaTeX labels")

    def test_latex_environment_dropped(self):
        o = "\\begin{table}\\end{table}\\begin{figure}\\end{figure}"
        self.assertFails(o, "\\begin{table}\\end{table}", "LaTeX environments")

    def test_declaration_section_locked(self):
        o = "## Results\nx\n## Data availability\nData are on request.\n## References\n"
        r = "## Results\nx\n## Data availability\nData are available on request.\n## References\n"
        self.assertFails(o, r, "Locked declaration sections (AI use, data availability, funding, ethics, ...)")

    def test_protect_terms(self):
        self.assertFails("landscape ecology matters", "ecology matters", "Protected terms (--protect)",
                         protect=["landscape ecology"])

    def test_url_removed(self):
        self.assertFails("at https://x.example/a.", "at the site.", "URLs")


class AcceptTests(unittest.TestCase):
    def test_accept_waives_a_named_difference(self):
        report, code = check("ages 13-17 here", "ages 13-17 years here", accept=["17 years"])
        self.assertEqual(code, 0, report)
        self.assertIn("ACCEPTED", report)

    def test_unused_accept_is_reported(self):
        report, _ = check("same", "same", accept=["ghost"])
        self.assertIn("Unused --accept", report)


class CheckTierTests(unittest.TestCase):
    def test_direction_flip_flagged_not_failed(self):
        report, code = check("Accuracy increased by 3 points.", "Accuracy decreased by 3 points.")
        self.assertEqual(code, 0, report)
        self.assertIn("check no effect changed direction", report)

    def test_causal_upgrade_visible(self):
        report, _ = check("X was associated with Y.", "X causes Y.")
        self.assertIn("`causes` 0->1", report)
        self.assertIn("`associated` 1->0", report)

    def test_planned_to_done_visible(self):
        report, _ = check("We will add experiments.", "We have added experiments.")
        self.assertIn("`will` 1->0", report)

    def test_number_order_swap_flagged(self):
        report, code = check("A was 71% and B was 54%.", "A was 54% and B was 71%.")
        self.assertIn("Number order", report)

    def test_number_word_change(self):
        report, _ = check("three datasets", "two datasets")
        self.assertIn("`three` 1->0", report)


if __name__ == "__main__":
    unittest.main()
