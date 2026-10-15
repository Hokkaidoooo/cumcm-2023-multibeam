"""独立于布线递推的区间并集及重叠检验。"""
from dataclasses import asdict, dataclass
from math import isfinite

from .geometry import PlanarSeabed, cross_section_swath, finite

TOLERANCE_M = 1e-8
RATE_TOLERANCE = 1e-10


@dataclass(frozen=True)
class Strip:
    center_m: float
    left_m: float
    right_m: float


def strip_at(seabed: PlanarSeabed, x_m: float, opening_deg: float = 120) -> Strip:
    if seabed.gradient_y != 0:
        raise ValueError("parallel-strip model requires constant depth along each north-south line")
    left, right = cross_section_swath(seabed.depth(x_m), seabed.gradient_x, opening_deg).interval(x_m)
    return Strip(x_m, left, right)


def audit_strips(strips: list[Strip], target_m: tuple[float, float], min_overlap: float = .1, max_overlap: float = .2) -> dict:
    """同时报告论文的半幅和分母，以及按前/后完整条带宽度归一化的交集。"""
    start, end = target_m
    if not all(isfinite(x) for x in (start, end, min_overlap, max_overlap)):
        raise ValueError("target and overlap bounds must be finite")
    if start >= end or not 0 <= min_overlap <= max_overlap < 1:
        raise ValueError("invalid target interval or overlap range")
    if not strips:
        raise ValueError("at least one strip is required")
    if any(not all(isfinite(x) for x in (s.center_m, s.left_m, s.right_m)) or not s.left_m < s.center_m < s.right_m for s in strips):
        raise ValueError("each strip must have finite left < center < right")
    ordered = sorted(strips, key=lambda s: s.center_m)
    if any(a.center_m == b.center_m for a, b in zip(ordered, ordered[1:])):
        raise ValueError("duplicate line centers")
    gaps = []
    cursor = start
    for strip in sorted(ordered, key=lambda s: s.left_m):
        left, right = max(start, strip.left_m), min(end, strip.right_m)
        if right <= start or left >= end:
            continue
        if left > cursor + TOLERANCE_M:
            gaps.append([cursor, left])
        cursor = max(cursor, right)
    if cursor < end - TOLERANCE_M:
        gaps.append([cursor, end])
    pairs = []
    for previous, current in zip(ordered, ordered[1:]):
        signed = min(previous.right_m, current.right_m) - max(previous.left_m, current.left_m)
        facing = previous.right_m - previous.center_m + current.center_m - current.left_m
        paper_rate = 1 - (current.center_m - previous.center_m) / facing
        rates = [paper_rate, signed / (previous.right_m - previous.left_m), signed / (current.right_m - current.left_m)]
        pairs.append({
            "previous_center_m": previous.center_m, "current_center_m": current.center_m,
            "signed_intersection_m": signed, "paper_facing_halves_rate": rates[0],
            "previous_full_width_rate": rates[1], "current_full_width_rate": rates[2],
            "within_all_definitions": all(min_overlap - RATE_TOLERANCE <= rate <= max_overlap + RATE_TOLERANCE for rate in rates),
        })
    return {
        "target_m": list(target_m), "overlap_range": [min_overlap, max_overlap],
        "fully_covered": not gaps, "uncovered_intervals_m": gaps,
        "uncovered_length_m": sum(right - left for left, right in gaps),
        "overlap_satisfied": all(p["within_all_definitions"] for p in pairs),
        "strips": [asdict(s) for s in ordered], "adjacent_pairs": pairs,
    }


def parallel_lines(seabed: PlanarSeabed, width_m: float, facing_overlap: float, opening_deg: float = 120) -> list[Strip]:
    """固定相邻半幅和重叠率的递推；保留第一条到达东界的测线。"""
    finite(width_m, "width_m")
    finite(facing_overlap, "facing_overlap")
    if width_m <= 0 or not 0 <= facing_overlap < 1:
        raise ValueError("positive width and 0 <= overlap < 1 are required")
    if seabed.gradient_y != 0:
        raise ValueError("depth must be constant along each line")
    seabed.depth(width_m)
    unit = cross_section_swath(1, seabed.gradient_x, opening_deg)
    left_factor, right_factor = unit.negative_m, unit.positive_m
    slope = seabed.gradient_x
    x = left_factor * seabed.depth_origin_m / (1 - left_factor * slope)
    lines = []
    while True:
        if not 0 <= x <= width_m:
            raise ValueError("this spacing places a line outside the target; choose another overlap")
        strip = strip_at(seabed, x, opening_deg)
        lines.append(strip)
        if strip.right_m >= width_m:
            return lines
        fraction = 1 - facing_overlap
        step = fraction * (left_factor + right_factor) * seabed.depth(x) / (1 - fraction * left_factor * slope)
        if not isfinite(step) or step <= 0 or x + step <= x:
            raise ValueError("line recurrence does not advance")
        x += step
