import pytest

from pam.samplers import attributes


@pytest.fixture
def michael():

    return {
        'age': 16,
        'agebin': 'younger',
        'gender': 'male'
    }


@pytest.fixture
def kasia():

    return {
        'age': 96,
        'agebin': 'older',
        'gender': 'female'
    }


@pytest.fixture
def fred():

    return {
        'age': -3,
        'agebin': '',
        'gender': 1
    }


@pytest.fixture
def bins():

    return {
        (0,50): 'younger',
        (51,100): 'older'
    }


@pytest.fixture
def cat_joint_distribution():

    mapping = ['agebin', 'gender']
    distribution = {
        'younger': {'male': 0, 'female': 0},
        'older': {'male': 0, 'female': 1}
    }
    return mapping, distribution


def test_apply_bin_integer_transformer_to_michael(michael, bins):
    assert attributes.bin_integer_transformer(michael, 'age', bins) == 'younger'


def test_apply_bin_integer_transformer_with_missing_bin(fred, bins):
    assert attributes.bin_integer_transformer(fred, 'age', bins) is None


def test_apply_discrete_joint_distribution_sampler_to_michael(michael, cat_joint_distribution):
    mapping, dist = cat_joint_distribution
    assert attributes.discrete_joint_distribution_sampler(michael, mapping, dist) == False


def test_applt_discrete_joint_distribution_sampler_to_kasia(kasia, cat_joint_distribution):
    mapping, dist = cat_joint_distribution
    assert attributes.discrete_joint_distribution_sampler(kasia, mapping, dist) == True


def test_applt_discrete_joint_distribution_sampler_to_fred_carefully(fred, cat_joint_distribution):
    mapping, dist = cat_joint_distribution
    with pytest.raises(KeyError):
        attributes.discrete_joint_distribution_sampler(fred, mapping, dist, careful=True)


def test_applt_discrete_joint_distribution_sampler_to_fred_not_carefully(fred, cat_joint_distribution):
    mapping, dist = cat_joint_distribution
    assert attributes.discrete_joint_distribution_sampler(fred, mapping, dist) == False
