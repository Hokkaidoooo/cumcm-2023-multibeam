import math
import unittest

from multibeam.geometry import PlanarSeabed, cross_section_swath


class GeometryTests(unittest.TestCase):
    def test_flat_bottom_analytic(self):
        for opening in (30, 90, 120, 170):
            with self.subTest(opening=opening):
                swath = cross_section_swath(100, 0, opening)
                self.assertAlmostEqual(swath.horizontal_width_m, 200 * math.tan(math.radians(opening / 2)))
                self.assertEqual(swath.horizontal_width_m, swath.seabed_width_m)

    def test_independent_3d_ray_plane_intersections(self):
        # 直接构造三维射线，与 z=D0+gx*x+gy*y 求交，不调用覆盖宽度推导。
        seabed = PlanarSeabed(100, .02, -.03)
        for heading in (0, 45, 90, 135, 180, 270, 315):
            with self.subTest(heading=heading):
                angle = math.radians(heading)
                normal = (-math.sin(angle), math.cos(angle))
                depth = 100 + .02 * 20 - .03 * -30
                distances = []
                for direction in (-1, 1):
                    dx = direction * math.sin(math.pi / 3) * normal[0]
                    dy = direction * math.sin(math.pi / 3) * normal[1]
                    dz = math.cos(math.pi / 3)
                    parameter = depth / (dz - .02 * dx + .03 * dy)
                    hit_x, hit_y, hit_z = 20 + parameter * dx, -30 + parameter * dy, parameter * dz
                    self.assertAlmostEqual(hit_z, 100 + .02 * hit_x - .03 * hit_y)
                    distances.append(math.hypot(hit_x - 20, hit_y + 30))
                swath = seabed.swath(20, -30, heading)
                self.assertAlmostEqual(swath.negative_m, distances[0])
                self.assertAlmostEqual(swath.positive_m, distances[1])

    def test_heading_reversal_swaps_sides(self):
        plane = PlanarSeabed(120, math.tan(math.radians(1.5)))
        a, b = plane.swath(0, 0, 90), plane.swath(0, 0, 270)
        self.assertAlmostEqual(a.negative_m, b.positive_m)
        self.assertAlmostEqual(a.positive_m, b.negative_m)
        self.assertAlmostEqual(a.horizontal_width_m, b.horizontal_width_m)

    def test_depth_is_vertical_and_distance_horizontal(self):
        plane = PlanarSeabed(110, -math.tan(math.radians(1.5)))
        self.assertAlmostEqual(plane.depth(100), 110 - 100 * math.tan(math.radians(1.5)))
        self.assertNotAlmostEqual(plane.depth(100), 110 - 100 * math.sin(math.radians(1.5)), places=5)

    def test_projection_and_scaling(self):
        a, b = cross_section_swath(50, .1), cross_section_swath(100, .1)
        self.assertAlmostEqual(b.horizontal_width_m, 2 * a.horizontal_width_m)
        self.assertAlmostEqual(a.seabed_width_m, a.horizontal_width_m * math.hypot(1, .1))

    def test_invalid_depths_and_angles_fail(self):
        cases = [(0, 0, 120), (-1, 0, 120), (float("nan"), 0, 120), (10, float("inf"), 120), (10, 0, 0), (10, 0, 180), (10, 0, float("nan"))]
        for case in cases:
            with self.subTest(case=case), self.assertRaises(ValueError):
                cross_section_swath(*case)
        with self.assertRaises(ValueError):
            PlanarSeabed(1, -.1).depth(10)

    def test_grazing_and_outward_beams_fail(self):
        tangent = math.tan(math.pi / 3)
        for slope in (-1 / tangent, 1 / tangent, 1):
            with self.subTest(slope=slope), self.assertRaises(ValueError):
                cross_section_swath(100, slope)

    def test_finite_inputs_cannot_return_infinite_results(self):
        with self.assertRaisesRegex(ValueError, "computed_depth_m must be finite"):
            PlanarSeabed(100, 1e308).depth(1e308)
        near_grazing = math.nextafter(1 / math.tan(math.pi / 3), 0)
        with self.assertRaisesRegex(ValueError, "extent_m must be finite"):
            cross_section_swath(1e308, near_grazing)
        with self.assertRaisesRegex(ValueError, "horizontal_width_m must be finite"):
            cross_section_swath(1e308, 0, 90)

    def test_seabed_length_avoids_unnecessary_squared_overflow(self):
        result = cross_section_swath(10, 1e200, 1e-205)
        self.assertTrue(math.isfinite(result.seabed_width_m))
        self.assertGreater(result.seabed_width_m, 0)


if __name__ == "__main__":
    unittest.main()
