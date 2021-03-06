import pytest
from datetime import datetime, timedelta

from pam.core import Population, Household, Person
from pam.activity import Plan, Activity, Leg
from pam.utils import minutes_to_datetime as mtdt
from pam.utils import timedelta_to_matsim_time as tdtm

from pam import PAMSequenceValidationError


testdata = [
    (0, datetime(1900, 1, 1, 0, 0)),
    (30, datetime(1900, 1, 1, 0, 30)),
    (300, datetime(1900, 1, 1, 5, 0)),
    (330, datetime(1900, 1, 1, 5, 30)),
]


@pytest.mark.parametrize("m,expected", testdata)
def test_minutes_to_dt(m, expected):
    assert mtdt(m) == expected


testdata = [
    (timedelta(seconds=0), "00:00:00"),
    (timedelta(hours=1), "01:00:00"),
    (timedelta(hours=11, minutes=1, seconds=3), "11:01:03"),
]


@pytest.mark.parametrize("td,expected", testdata)
def test_td_to_matsim_string(td, expected):
    assert tdtm(td) == expected


def test_population_add_household():
    population = Population()
    household = Household('1')
    population.add(household)
    assert len(population.households) == 1
    assert list(population.households) == ['1']


def test_household_add_person():
    household = Household('1')
    person = Person('1')
    person.add(Activity(1, 'home', 1, start_time=0))
    household.add(person)
    assert len(household.people) == 1
    assert list(household.people) == ['1']


def test_person_add_activity():
    person = Person('1')
    act = Activity(1, 'home', 1)
    person.add(act)
    assert len(person.plan) == 1


def test_person_add_leg():
    person = Person('1')
    act = Activity(1, 'home', 1)
    person.add(act)
    leg = Leg(1, 'car', start_area=1, end_area=2)
    person.add(leg)
    assert len(person.plan) == 2


def test_person_add_activity_activity_raise_error():
    person = Person('1')
    act = Activity(1, 'home', 1)
    person.add(act)
    act = Activity(2, 'work', 1)
    with pytest.raises(PAMSequenceValidationError):
        person.add(act)


def test_person_add_leg_first_raise_error():
    person = Person('1')
    leg = Leg(1, 'car', start_area=1, end_area=2)
    with pytest.raises(PAMSequenceValidationError):
        person.add(leg)


def test_person_add_leg_leg_raise_error():
    person = Person('1')
    act = Activity(1, 'home', 1)
    person.add(act)
    leg = Leg(1, 'car', start_area=1, end_area=2)
    person.add(leg)
    leg = Leg(2, 'car', start_area=2, end_area=1)
    with pytest.raises(PAMSequenceValidationError):
        person.add(leg)


def test_person_home_based():
    person = Person('1')
    person.add(Activity(1, 'home', 1))
    person.add(Leg(1, 'car', start_area=1, end_area=2))
    person.add(Activity(2, 'work', 1))
    person.add(Leg(2, 'car', start_area=2, end_area=1))
    person.add(Activity(3, 'home', 1))
    assert person.home_based


def test_person_not_home_based():
    person = Person('1')
    person.add(Activity(1, 'work', 1))
    person.add(Leg(1, 'car', start_area=1, end_area=2))
    person.add(Activity(2, 'home', 1))
    person.add(Leg(2, 'car', start_area=2, end_area=1))
    person.add(Activity(3, 'work', 1))
    assert not person.home_based


def test_person_closed_plan():
    person = Person('1')
    person.add(Activity(1, 'home', 1))
    person.add(Leg(1, 'car', start_area=1, end_area=2))
    person.add(Activity(2, 'work', 1))
    person.add(Leg(2, 'car', start_area=2, end_area=1))
    person.add(Activity(3, 'home', 1))
    assert person.closed_plan


def test_person_not_closed_plan_different_acts():
    person = Person('1')
    person.add(Activity(1, 'work', 1))
    person.add(Leg(1, 'car', start_area=1, end_area=2))
    person.add(Activity(2, 'home', 1))
    assert not person.closed_plan


def test_person_not_closed_plan_different_areas():
    person = Person('1')
    person.add(Activity(1, 'work', 1))
    person.add(Leg(1, 'car', start_area=1, end_area=2))
    person.add(Activity(2, 'home', 1))
    person.add(Leg(2, 'car', start_area=2, end_area=3))
    person.add(Activity(3, 'work', 3))
    assert not person.closed_plan
