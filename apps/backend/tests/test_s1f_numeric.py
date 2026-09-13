from decimal import Decimal

import pytest

from hct_backend.s1f_numeric import (
    DecimalValue,
    NumericFailureReason,
    NumericPolicyError,
    require_non_negative,
    require_price,
    require_quantity,
    validate_ohlc,
)


def test_decimal_text_is_canonical_and_retains_material_scale() -> None:
    value = DecimalValue.parse("1.2300")
    assert value.canonical_text == "1.23"
    assert value.material_scale == 4
    assert value.fingerprint != DecimalValue.parse("1.23").fingerprint


@pytest.mark.parametrize(
    ("raw", "reason"),
    [
        (1.0, NumericFailureReason.BINARY_FLOAT),
        ("1e-3", NumericFailureReason.MALFORMED),
        ("NaN", NumericFailureReason.MALFORMED),
        ("Infinity", NumericFailureReason.MALFORMED),
        ("1.1234567890123456789", NumericFailureReason.SCALE_OVERFLOW),
    ],
)
def test_decimal_policy_rejects_unsafe_inputs(raw: object, reason: NumericFailureReason) -> None:
    with pytest.raises(NumericPolicyError) as error:
        DecimalValue.parse(raw)  # type: ignore[arg-type]
    assert error.value.reason is reason


def test_scaled_integer_is_exact_and_prices_quantities_are_restrictive() -> None:
    assert DecimalValue.scaled_integer(123, 2).canonical_text == "1.23"
    assert require_price("1").value == Decimal("1")
    assert require_quantity("0").value == Decimal("0")
    with pytest.raises(NumericPolicyError) as error:
        require_price("0")
    assert error.value.reason is NumericFailureReason.NON_POSITIVE_PRICE
    with pytest.raises(NumericPolicyError) as error:
        require_quantity("-1")
    assert error.value.reason is NumericFailureReason.NEGATIVE_QUANTITY


def test_ohlc_bounds_are_fail_closed() -> None:
    good = [DecimalValue.parse(item) for item in ("10", "12", "9", "11")]
    validate_ohlc(*good)
    with pytest.raises(NumericPolicyError) as error:
        validate_ohlc(
            DecimalValue.parse("10"),
            DecimalValue.parse("8"),
            DecimalValue.parse("9"),
            DecimalValue.parse("10"),
        )
    assert error.value.reason is NumericFailureReason.IMPOSSIBLE_OHLC


@pytest.mark.parametrize(
    ("raw", "reason"),
    [
        (True, NumericFailureReason.BINARY_FLOAT),
        (object(), NumericFailureReason.MALFORMED),
        ("1" * 39, NumericFailureReason.PRECISION_OVERFLOW),
        ("1.0000000000000000001", NumericFailureReason.SCALE_OVERFLOW),
        ("1" + "0" * 20, NumericFailureReason.INTEGER_DIGITS_OVERFLOW),
    ],
)
def test_decimal_policy_rejects_types_and_bounds(raw: object, reason: NumericFailureReason) -> None:
    with pytest.raises(NumericPolicyError) as error:
        DecimalValue.parse(raw)  # type: ignore[arg-type]
    assert error.value.reason is reason


def test_decimal_constructor_and_nonnegative_policy_are_fail_closed() -> None:
    with pytest.raises(NumericPolicyError):
        DecimalValue(Decimal("NaN"), "1", 0)
    with pytest.raises(NumericPolicyError):
        DecimalValue(Decimal("1"), "1e0", 0)
    with pytest.raises(NumericPolicyError):
        DecimalValue(Decimal("1"), "1", True)  # type: ignore[arg-type]
    with pytest.raises(NumericPolicyError):
        DecimalValue(Decimal("1"), "1", 19)
    assert DecimalValue.parse(Decimal("1.20")).material_scale == 2
    assert DecimalValue.parse("-0.00").canonical_text == "0"
    with pytest.raises(NumericPolicyError) as error:
        DecimalValue.scaled_integer(True, 1)  # type: ignore[arg-type]
    assert error.value.reason is NumericFailureReason.MALFORMED
    with pytest.raises(NumericPolicyError) as error:
        DecimalValue.scaled_integer(1, 19)
    assert error.value.reason is NumericFailureReason.SCALE_OVERFLOW
    with pytest.raises(NumericPolicyError) as error:
        require_non_negative("-1")
    assert error.value.reason is NumericFailureReason.NEGATIVE_VALUE


def test_numeric_policy_rejects_bad_ohlc_and_mixed_inputs() -> None:
    good = DecimalValue.parse("1")
    with pytest.raises(NumericPolicyError):
        validate_ohlc(DecimalValue.parse("0"), good, good, good)
    with pytest.raises(NumericPolicyError):
        validate_ohlc(good, DecimalValue.parse("1"), DecimalValue.parse("2"), good)
