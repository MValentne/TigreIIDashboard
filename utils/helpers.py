"""General helper utilities used across the dashboard."""

from __future__ import annotations

from typing import Final

ALPHA_DEFAULT: Final[float] = 0.05


def format_p_value(p_value: float, precision: int = 4) -> str:
    """Format a p-value for presentation."""
    if p_value < 0.001:
        return "< 0.001"
    return f"= {p_value:.{precision}f}"


def interpret_significance(p_value: float, alpha: float = ALPHA_DEFAULT) -> str:
    """Return a short significance interpretation."""
    if p_value < alpha:
        return f"Se rechaza H0 porque p {format_p_value(p_value)} < {alpha:.2f}."
    return f"No se rechaza H0 porque p {format_p_value(p_value)} >= {alpha:.2f}."


def strength_label(value: float) -> str:
    """Classify the strength of a correlation coefficient."""
    magnitude = abs(value)
    if magnitude < 0.2:
        return "muy débil"
    if magnitude < 0.4:
        return "débil"
    if magnitude < 0.6:
        return "moderada"
    if magnitude < 0.8:
        return "fuerte"
    return "muy fuerte"


def trend_label(value: float) -> str:
    """Return the sign-based trend for a coefficient."""
    return "positiva" if value >= 0 else "negativa"


def regression_equation(intercept: float, slope: float) -> str:
    """Format a linear regression equation."""
    sign = "+" if slope >= 0 else "-"
    return f"y = {intercept:.2f} {sign} {abs(slope):.2f}x"
