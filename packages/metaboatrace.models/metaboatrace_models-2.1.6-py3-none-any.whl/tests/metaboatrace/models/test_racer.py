from datetime import date

import pytest
from pydantic import ValidationError

from metaboatrace.models.racer import Gender, Racer, RacerCondition, RacerRank
from metaboatrace.models.region import Branch, Prefecture


@pytest.mark.parametrize(
    "last_name,first_name,gender,term,birth_date,height,born_prefecture,branch,current_rating,expected",
    [
        (
            "泥沼",
            "亀之助",
            Gender.MALE,
            10,
            date.today(),
            170,
            Prefecture.TOKYO,
            Branch.TOKYO,
            RacerRank.A1,
            True,
        ),  # valid case
        (
            123,
            "亀之助",
            Gender.MALE,
            10,
            date.today(),
            170,
            Prefecture.TOKYO,
            Branch.TOKYO,
            RacerRank.A1,
            False,
        ),  # invalid last_name
        (
            "泥沼",
            123,
            Gender.MALE,
            10,
            date.today(),
            170,
            Prefecture.TOKYO,
            Branch.TOKYO,
            RacerRank.A1,
            False,
        ),  # invalid first_name
        (
            "泥沼",
            "亀之助",
            "MALE",
            10,
            date.today(),
            170,
            Prefecture.TOKYO,
            Branch.TOKYO,
            RacerRank.A1,
            False,
        ),  # invalid gender
        (
            "泥沼",
            "亀之助",
            Gender.MALE,
            "10",
            date.today(),
            170,
            Prefecture.TOKYO,
            Branch.TOKYO,
            RacerRank.A1,
            False,
        ),  # invalid term
        (
            "泥沼",
            "亀之助",
            Gender.MALE,
            10,
            date.today(),
            170,
            Prefecture.TOKYO,
            Branch.TOKYO,
            "A1",
            False,
        ),  # invalid current_rating
    ],
)
def test_racer(  # type: ignore
    last_name,
    first_name,
    gender,
    term,
    birth_date,
    height,
    born_prefecture,
    branch,
    current_rating,
    expected,
):
    data = {
        "registration_number": 12345,
        "last_name": last_name,
        "first_name": first_name,
        "gender": gender,
        "term": term,
        "birth_date": birth_date,
        "height": height,
        "born_prefecture": born_prefecture,
        "branch": branch,
        "current_rating": current_rating,
    }
    if expected:
        Racer(**data)
    else:
        with pytest.raises(ValidationError):
            Racer(**data)


@pytest.mark.parametrize(
    "recorded_on,racer_registration_number,weight,adjust,expected",
    [
        (date.today(), 12345, 60, 0.0, True),  # valid case
        (123, 12345, 60, 0.0, False),  # invalid recorded_on
        (date.today(), "12345", 60, 0.0, False),  # invalid racer_registration_number
        (date.today(), 12345, "六十", 0.0, False),  # invalid weight
        (date.today(), 12345, 60, "invalid", False),  # invalid adjust
    ],
)
def test_racer_condition(recorded_on, racer_registration_number, weight, adjust, expected):  # type: ignore
    data = {
        "recorded_on": recorded_on,
        "racer_registration_number": racer_registration_number,
        "weight": weight,
        "adjust": adjust,
    }
    if expected:
        RacerCondition(**data)
    else:
        with pytest.raises(ValidationError):
            RacerCondition(**data)
