import pytest

from daycare_fees import enrolment_allowed, extra_hours_fee, pickup_status


@pytest.mark.parametrize(
    ("age_group", "hours", "has_sibling", "expected"),
    [
        ("toddler", 25, False, 0),
        ("preschool", 35, True, 0),
        ("infant", 21, False, 14),
        ("preschool", 31, False, 9),
        ("toddler", 46, False, 294),
        ("infant", 41, False, 462),
    ],
)
def test_extra_hours_fee_covers_fee_calculation_branches(
    age_group, hours, has_sibling, expected
):
    assert extra_hours_fee(age_group, hours, has_sibling) == expected


def test_extra_hours_fee_does_not_apply_sibling_adjustment_to_infant():
    assert extra_hours_fee("infant", 21, True) == 14


def test_extra_hours_fee_rejects_an_unknown_age_group():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("school_age", 10, False)


def test_extra_hours_fee_rejects_negative_hours():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("toddler", -1, False)


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
def test_enrolment_allowed_covers_all_decision_outcomes(
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
def test_pickup_status_covers_cutoff_and_status_branches(
    minutes_left, is_aftercare, is_friday, expected
):
    assert pickup_status(minutes_left, is_aftercare, is_friday) == expected
