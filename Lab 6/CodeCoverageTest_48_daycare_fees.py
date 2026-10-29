import pytest

from daycare_fees import enrolment_allowed, extra_hours_fee, pickup_status


def test_extra_hours_fee_rejects_unknown_age_group():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("school_age", 10, False)


def test_extra_hours_fee_rejects_negative_hours():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("toddler", -1, False)


def test_extra_hours_fee_returns_zero_at_standard_included_limit():
    assert extra_hours_fee("toddler", 25, False) == 0


def test_extra_hours_fee_applies_sibling_hours_to_non_infant():
    assert extra_hours_fee("preschool", 35, True) == 0


def test_extra_hours_fee_uses_infant_base_rate():
    assert extra_hours_fee("infant", 21, True) == 14


def test_extra_hours_fee_uses_non_infant_base_rate():
    assert extra_hours_fee("preschool", 31, False) == 9


def test_extra_hours_fee_increases_non_infant_rate_after_twenty_extra_hours():
    assert extra_hours_fee("toddler", 46, False) == 294


def test_extra_hours_fee_applies_infant_surcharge_after_twenty_extra_hours():
    assert extra_hours_fee("infant", 41, False) == 462


@pytest.mark.parametrize(
    ("age_months", "vacancies", "is_immunisation_pending", "expected"),
    [
        (12, 0, True, True),
        (11, 5, True, False),
        (5, 3, False, False),
        (6, 0, False, False),
        (6, 1, False, True),
    ],
)
def test_enrolment_allowed_covers_age_immunisation_and_vacancy_rules(
    age_months, vacancies, is_immunisation_pending, expected
):
    assert (
        enrolment_allowed(age_months, vacancies, is_immunisation_pending)
        is expected
    )


@pytest.mark.parametrize(
    ("minutes_left", "is_aftercare", "is_friday", "expected"),
    [
        (10, False, False, "on_time"),
        (-5, False, False, "late"),
        (-6, False, False, "overdue"),
        (20, True, False, "on_time"),
        (15, True, True, "late"),
        (14, True, True, "overdue"),
        (20, False, True, "on_time"),
    ],
)
def test_pickup_status_covers_cutoffs_and_all_statuses(
    minutes_left, is_aftercare, is_friday, expected
):
    assert pickup_status(minutes_left, is_aftercare, is_friday) == expected
