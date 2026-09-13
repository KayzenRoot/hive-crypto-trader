"""Fail-closed Decimal policy for the S1F public market-value plane."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Final

_DECIMAL_TEXT: Final = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$")
_INTEGER_TEXT: Final = re.compile(r"^(?:0|[1-9][0-9]*)$")


class NumericFailureReason(StrEnum):
    MALFORMED = "MALFORMED"
    BINARY_FLOAT = "BINARY_FLOAT_REJECTED"
    NON_FINITE = "NON_FINITE"
    PRECISION_OVERFLOW = "PRECISION_OVERFLOW"
    SCALE_OVERFLOW = "SCALE_OVERFLOW"
    INTEGER_DIGITS_OVERFLOW = "INTEGER_DIGITS_OVERFLOW"
    NON_POSITIVE_PRICE = "NON_POSITIVE_PRICE"
    NEGATIVE_QUANTITY = "NEGATIVE_QUANTITY"
    IMPOSSIBLE_OHLC = "IMPOSSIBLE_OHLC"
    NEGATIVE_VALUE = "NEGATIVE_VALUE"


class NumericPolicyError(ValueError):
    """Typed failure for a value that cannot enter an authoritative boundary."""

    def __init__(self, reason: NumericFailureReason, message: str) -> None:
        self.reason = reason
        super().__init__(f"{reason.value}: {message}")


class NumericPolicy:
    VERSION = "DECIMAL_TEXT_V1"
    MAX_PRECISION = 38
    MAX_SCALE = 18
    MAX_INTEGER_DIGITS = 20


def _fingerprint(material: object) -> str:
    encoded = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _canonical_material(value: Decimal) -> tuple[str, int]:
    """Return the canonical text and the scale carried by the Decimal input."""

    if not value.is_finite():
        raise NumericPolicyError(NumericFailureReason.NON_FINITE, "finite Decimal required")
    exponent = value.as_tuple().exponent
    if not isinstance(exponent, int):
        raise NumericPolicyError(
            NumericFailureReason.NON_FINITE, "non-finite Decimal exponent is forbidden"
        )
    material_scale = max(-exponent, 0)
    canonical = format(value, "f")
    if "." in canonical:
        canonical = canonical.rstrip("0").rstrip(".")
    if canonical in {"", "-0"} or canonical == "-0.0":
        canonical = "0"
    if canonical.startswith("-") and Decimal(canonical) == 0:
        canonical = "0"
    integer_part = canonical.partition(".")[0].lstrip("-").lstrip("0")
    integer_digits = len(integer_part)
    precision = max(len(value.as_tuple().digits), integer_digits + material_scale)
    if precision > NumericPolicy.MAX_PRECISION:
        raise NumericPolicyError(NumericFailureReason.PRECISION_OVERFLOW, "precision exceeds 38")
    if material_scale > NumericPolicy.MAX_SCALE:
        raise NumericPolicyError(NumericFailureReason.SCALE_OVERFLOW, "scale exceeds 18")
    if integer_digits > NumericPolicy.MAX_INTEGER_DIGITS:
        raise NumericPolicyError(
            NumericFailureReason.INTEGER_DIGITS_OVERFLOW, "integer digits exceed 20"
        )
    return canonical, material_scale


@dataclass(frozen=True, slots=True)
class DecimalValue:
    """Exact Decimal plus its material input scale and canonical text."""

    value: Decimal
    canonical_text: str
    material_scale: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, Decimal) or not self.value.is_finite():
            raise NumericPolicyError(NumericFailureReason.NON_FINITE, "finite Decimal required")
        if not isinstance(self.canonical_text, str) or not _DECIMAL_TEXT.fullmatch(
            self.canonical_text
        ):
            raise NumericPolicyError(NumericFailureReason.MALFORMED, "canonical text is invalid")
        if isinstance(self.material_scale, bool) or not isinstance(self.material_scale, int):
            raise NumericPolicyError(NumericFailureReason.MALFORMED, "material scale is invalid")
        canonical, material_scale = _canonical_material(self.value)
        if self.canonical_text != canonical or self.material_scale != material_scale:
            raise NumericPolicyError(
                NumericFailureReason.MALFORMED,
                "canonical text and material scale do not match Decimal material",
            )

    @classmethod
    def parse(cls, raw: str | int | Decimal) -> DecimalValue:
        if isinstance(raw, bool) or isinstance(raw, float):
            raise NumericPolicyError(
                NumericFailureReason.BINARY_FLOAT, "binary float input is forbidden"
            )
        if isinstance(raw, int):
            text = str(raw)
        elif isinstance(raw, Decimal):
            text = format(raw, "f")
        elif isinstance(raw, str):
            text = raw
        else:
            raise NumericPolicyError(NumericFailureReason.MALFORMED, "Decimal text is required")
        if not _DECIMAL_TEXT.fullmatch(text):
            raise NumericPolicyError(
                NumericFailureReason.MALFORMED, "base-10 text without exponent is required"
            )
        try:
            value = Decimal(text)
        except InvalidOperation as exc:
            raise NumericPolicyError(
                NumericFailureReason.MALFORMED, "Decimal text cannot be parsed"
            ) from exc
        if not value.is_finite():
            raise NumericPolicyError(
                NumericFailureReason.NON_FINITE, "NaN and Infinity are forbidden"
            )
        canonical, material_scale = _canonical_material(value)
        return cls(value=value, canonical_text=canonical, material_scale=material_scale)

    @classmethod
    def scaled_integer(cls, unscaled: int, scale: int) -> DecimalValue:
        if (
            isinstance(unscaled, bool)
            or not isinstance(unscaled, int)
            or not isinstance(scale, int)
        ):
            raise NumericPolicyError(
                NumericFailureReason.MALFORMED, "integer and scale are required"
            )
        if scale < 0 or scale > NumericPolicy.MAX_SCALE:
            raise NumericPolicyError(NumericFailureReason.SCALE_OVERFLOW, "scale exceeds 18")
        return cls.parse(Decimal(unscaled).scaleb(-scale))

    @property
    def fingerprint(self) -> str:
        return _fingerprint(
            {
                "policy": NumericPolicy.VERSION,
                "canonical_text": self.canonical_text,
                "material_scale": self.material_scale,
            }
        )

    def __str__(self) -> str:
        return self.canonical_text


def require_price(raw: str | int | Decimal) -> DecimalValue:
    value = DecimalValue.parse(raw)
    if value.value <= 0:
        raise NumericPolicyError(NumericFailureReason.NON_POSITIVE_PRICE, "price must be positive")
    return value


def require_quantity(raw: str | int | Decimal) -> DecimalValue:
    value = DecimalValue.parse(raw)
    if value.value < 0:
        raise NumericPolicyError(
            NumericFailureReason.NEGATIVE_QUANTITY, "quantity cannot be negative"
        )
    return value


def require_non_negative(raw: str | int | Decimal) -> DecimalValue:
    value = DecimalValue.parse(raw)
    if value.value < 0:
        raise NumericPolicyError(NumericFailureReason.NEGATIVE_VALUE, "value cannot be negative")
    return value


def validate_ohlc(
    open_value: DecimalValue,
    high: DecimalValue,
    low: DecimalValue,
    close: DecimalValue,
) -> None:
    values = (open_value, high, low, close)
    if any(not isinstance(item, DecimalValue) or item.value <= 0 for item in values):
        raise NumericPolicyError(
            NumericFailureReason.IMPOSSIBLE_OHLC, "OHLC prices must be positive"
        )
    if high.value < max(open_value.value, close.value, low.value) or low.value > min(
        open_value.value, close.value, high.value
    ):
        raise NumericPolicyError(
            NumericFailureReason.IMPOSSIBLE_OHLC, "OHLC bounds are contradictory"
        )


def ensure_same_numeric_policy(*values: DecimalValue) -> None:
    if any(not isinstance(value, DecimalValue) for value in values):
        raise NumericPolicyError(NumericFailureReason.MALFORMED, "DecimalValue is required")
    if {NumericPolicy.VERSION for _ in values} != {NumericPolicy.VERSION}:
        raise NumericPolicyError(NumericFailureReason.MALFORMED, "numeric policy differs")
