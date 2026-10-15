"""仅用于重现竞赛脚本的错误与比较历史结果，不用于产生新方案。

这些冻结公式是故意保留的独立历史基线；不可被生产几何函数调用。
"""
import math

from .coverage import Strip


def question2_value(beta_deg: float, distance_m: float) -> tuple[float, float]:
    """返回旧脚本的水平值及去掉投影因子后的值，保留旧括号错误。"""
    slope_deg = 1.5
    angles = []
    for beta in (beta_deg, beta_deg + 90):
        numerator = math.tan(math.radians(slope_deg))
        denominator = math.sqrt(1 + math.tan(math.radians(beta)) ** 2 + math.tan(math.radians(slope_deg) ** 2))
        angles.append(math.asin(numerator / denominator))
    along, across = angles
    sign = -1 if 90 < beta_deg < 270 else 1
    depth = 120 + sign * distance_m * math.tan(along)
    raw = depth * math.sin(math.radians(60)) * (1 / math.cos(math.radians(60) + across) + 1 / math.cos(across - math.radians(60)))
    return raw * math.cos(across), raw


def question3_strips() -> list[Strip]:
    """逐字保持旧常数、sin 深度式、0.9 步长和丢弃跨界末线规则。"""
    result = []
    x = 341.374978
    while True:
        depth = 206.9594 - x * math.sin(math.radians(1.5))
        left = depth / math.cos(math.radians(61.5)) * math.sin(math.radians(60)) * math.cos(math.radians(1.5))
        right = depth / math.cos(math.radians(-58.5)) * math.sin(math.radians(60)) * math.cos(math.radians(1.5))
        if x + right > 4 * 1852:
            return result
        result.append(Strip(x, x - left, x + right))
        x += .9 * (left + right)
