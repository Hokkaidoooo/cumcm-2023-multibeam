"""坐标均为水平米数；z 向下，水深为垂直距离。推导见 docs/geometry.md。"""
from dataclasses import dataclass
from math import cos, hypot, isfinite, radians, sin, tan


def finite(value: float, name: str) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite, got {value!r}")


@dataclass(frozen=True)
class Swath:
    depth_m: float
    cross_slope: float
    negative_m: float
    positive_m: float

    @property
    def horizontal_width_m(self) -> float:
        result = self.negative_m + self.positive_m
        finite(result, "horizontal_width_m")
        return result

    @property
    def seabed_width_m(self) -> float:
        result = self.horizontal_width_m * hypot(1, self.cross_slope)
        finite(result, "seabed_width_m")
        return result

    def interval(self, center_m: float) -> tuple[float, float]:
        finite(center_m, "center_m")
        return center_m - self.negative_m, center_m + self.positive_m


def cross_section_swath(depth_m: float, cross_slope: float, opening_deg: float = 120) -> Swath:
    """波束平面中的有符号坡度 k = dz/dq；两边波束必须正向交于海底。"""
    for value, name in ((depth_m, "depth_m"), (cross_slope, "cross_slope"), (opening_deg, "opening_deg")):
        finite(value, name)
    if depth_m <= 0:
        raise ValueError("depth_m must be positive")
    if not 0 < opening_deg < 180:
        raise ValueError("opening_deg must be between 0 and 180 degrees")
    tangent = tan(radians(opening_deg / 2))
    if abs(cross_slope * tangent) >= 1:
        raise ValueError("outer beam is parallel to or misses the seabed in its forward direction")
    negative = depth_m / (1 + cross_slope * tangent) * tangent
    positive = depth_m / (1 - cross_slope * tangent) * tangent
    finite(negative, "negative_extent_m")
    finite(positive, "positive_extent_m")
    if negative <= 0 or positive <= 0:
        raise ValueError("beam extent underflows floating-point precision")
    result = Swath(depth_m, cross_slope, negative, positive)
    _ = result.horizontal_width_m, result.seabed_width_m
    return result


@dataclass(frozen=True)
class PlanarSeabed:
    depth_origin_m: float
    gradient_x: float
    gradient_y: float = 0

    def __post_init__(self) -> None:
        for value, name in ((self.depth_origin_m, "depth_origin_m"), (self.gradient_x, "gradient_x"), (self.gradient_y, "gradient_y")):
            finite(value, name)
        if self.depth_origin_m <= 0:
            raise ValueError("depth_origin_m must be positive")

    def depth(self, x_m: float, y_m: float = 0) -> float:
        finite(x_m, "x_m")
        finite(y_m, "y_m")
        result = self.depth_origin_m + self.gradient_x * x_m + self.gradient_y * y_m
        finite(result, "computed_depth_m")
        if result <= 0:
            raise ValueError(f"nonpositive depth at ({x_m}, {y_m}): {result}")
        return result

    def swath(self, x_m: float, y_m: float, heading_deg: float, opening_deg: float = 120) -> Swath:
        """heading 从 +x 逆时针计；横测线正向为 (-sin heading, cos heading)。"""
        finite(heading_deg, "heading_deg")
        angle = radians(heading_deg)
        cross_slope = -self.gradient_x * sin(angle) + self.gradient_y * cos(angle)
        return cross_section_swath(self.depth(x_m, y_m), cross_slope, opening_deg)
