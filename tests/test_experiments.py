from math import radians, tan
from pathlib import Path
import unittest

from multibeam.coverage import Strip, audit_strips, parallel_lines
from multibeam.experiments import Q3_LENGTH_M, Q3_WIDTH_M, question1, question2, question3
from multibeam.geometry import PlanarSeabed
from multibeam.legacy import question3_strips

ROOT = Path(__file__).resolve().parents[1]


class CoverageTests(unittest.TestCase):
    def test_legacy_counterexample_remains_visible(self):
        strips = question3_strips()
        audit = audit_strips(strips, (0, Q3_WIDTH_M))
        self.assertEqual(len(strips), 32)
        self.assertEqual(len(strips) * Q3_LENGTH_M, 118528)
        self.assertAlmostEqual(audit["uncovered_length_m"], 15.7447, places=4)
        for pair in audit["adjacent_pairs"]:
            self.assertAlmostEqual(pair["paper_facing_halves_rate"], .059812, places=6)
        self.assertFalse(audit["fully_covered"])
        self.assertFalse(audit["overlap_satisfied"])

    def test_union_is_independent_of_line_order_and_finds_all_gaps(self):
        strips = [Strip(8, 7, 9), Strip(2, 1, 3), Strip(5, 4, 6)]
        audit = audit_strips(strips, (0, 10))
        self.assertEqual(audit["uncovered_intervals_m"], [[0, 1], [3, 4], [6, 7], [9, 10]])
        self.assertEqual(audit["uncovered_length_m"], 4)
        self.assertFalse(audit["overlap_satisfied"])

    def test_union_handles_containment_and_outside_intervals(self):
        audit = audit_strips([Strip(-3, -4, -2), Strip(5, -1, 11), Strip(6, 4, 8)], (0, 10))
        self.assertTrue(audit["fully_covered"])

    def test_invalid_strip_contract_fails(self):
        for strips in ([], [Strip(1, 1, 2)], [Strip(1, 0, 2), Strip(1, -1, 3)]):
            with self.subTest(strips=strips), self.assertRaises(ValueError):
                audit_strips(strips, (0, 10))

    def test_new_candidates_cover_and_satisfy_each_overlap_definition(self):
        result = question3()
        self.assertEqual(result["selected_line_count"], 34)
        self.assertEqual(result["selected_total_length_m"], 125936)
        for candidate in result["candidates"]:
            with self.subTest(overlap=candidate["facing_overlap"]):
                self.assertTrue(candidate["fully_covered"])
                self.assertTrue(candidate["overlap_satisfied"])
                self.assertEqual(candidate["uncovered_length_m"], 0)
                for pair in candidate["adjacent_pairs"]:
                    for field in ("paper_facing_halves_rate", "previous_full_width_rate", "current_full_width_rate"):
                        self.assertGreaterEqual(pair[field], .1)
                        self.assertLessEqual(pair[field], .2)

    def test_flat_seabed_spacing_analytic(self):
        strips = parallel_lines(PlanarSeabed(100, 0), 900, .15)
        width = 200 * tan(radians(60))
        self.assertAlmostEqual(strips[0].left_m, 0)
        self.assertAlmostEqual(strips[1].center_m - strips[0].center_m, .85 * width)

    def test_fixed_first_line_candidate_can_be_infeasible(self):
        # 固定首线贴左界和固定重叠率不是适用于任意宽度的全局优化器。
        with self.assertRaisesRegex(ValueError, "outside the target"):
            parallel_lines(PlanarSeabed(100, 0), 1000, .15)


class ExperimentTests(unittest.TestCase):
    def test_question1_reference_depth_and_negative_overlap(self):
        rows = question1()["rows"]
        self.assertEqual(len(rows), 9)
        self.assertEqual(rows[4]["depth_m"], 70)
        self.assertIsNone(rows[0]["paper_overlap_rate"])
        self.assertLess(rows[-1]["paper_overlap_rate"], 0)

    def test_question2_history_and_orthogonal_headings(self):
        result = question2(ROOT)
        self.assertEqual(result["legacy_mismatch_count"], 48)
        self.assertEqual(result["without_projection_match_count"], 64)
        self.assertAlmostEqual(result["legacy_max_absolute_difference_m"], .14279, places=5)
        expected = 240 * tan(radians(60)) / (1 - (tan(radians(1.5)) * tan(radians(60))) ** 2)
        for row in result["rows"]:
            if row["beta_deg"] in (90, 270):
                self.assertAlmostEqual(row["depth_m"], 120)
                self.assertAlmostEqual(row["corrected_horizontal_m"], expected)


if __name__ == "__main__":
    unittest.main()
