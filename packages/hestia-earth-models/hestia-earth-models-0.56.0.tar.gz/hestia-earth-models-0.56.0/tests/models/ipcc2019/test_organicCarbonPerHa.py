import json
import random

from unittest.mock import patch

from tests.utils import fixtures_path, fake_new_measurement

from hestia_earth.models.ipcc2019.organicCarbonPerHa import (
    MODEL,
    TERM_ID,
    CarbonSource,
    run,
    _calc_temperature_factor,
    _calc_water_factor,
    _run_annual_organic_carbon_inputs
)


TIER_2_SUBFOLDERS = [
    'Tier2/with-generalised-monthly-measurements',  # Closes issue 600
    'Tier2/with-incomplete-climate-data',  # Closes issue 599
    'Tier2/with-initial-soc',
    'Tier2/with-multi-year-cycles',
    'Tier2/without-any-measurements',  # Closes issue 594
    'Tier2/without-initial-soc'
]

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


def _load_cycles(path):
    with open(path, encoding='utf-8') as f:
        cycles = json.load(f)
    return cycles


def test_calc_temperature_factor(*args):
    NUM_RANDOM = 9999
    MIN_T, MAX_T = -60, 60
    MIN_FAC, MAX_FAC = 0, 1

    temperatures = [random.uniform(MIN_T, MAX_T) for _ in range(0, NUM_RANDOM)]
    results = [
        _calc_temperature_factor(t) for t in temperatures
    ]

    assert all(MIN_FAC <= result <= MAX_FAC for result in results)


def test_calc_water_factor(*args):
    NUM_RANDOM = 9999
    MIN, MAX = 0, 9999
    MIN_FAC, MAX_FAC = 0.2129, 1.5
    IRR_FAC = 0.775

    precipitations = [random.uniform(MIN, MAX) for _ in range(0, NUM_RANDOM)]
    pets = [random.uniform(MIN, MAX) for _ in range(0, NUM_RANDOM)]

    results = [
        _calc_water_factor(pre, pet) for pre, pet in zip(precipitations, pets)
    ]
    irr_results = [
        _calc_water_factor(pre, pet, is_irrigated=True) for pre, pet in zip(precipitations, pets)
    ]

    assert all(MIN_FAC <= result <= MAX_FAC for result in results)
    assert all(result == IRR_FAC for result in irr_results)
    assert _calc_water_factor(1, 1) == _calc_water_factor(1000, 1000)


def test_run_annual_organic_carbon_inputs(*args):
    """
    Test the _run_annual_organic_carbon_inputs model:

    As the IPCC don't provide any test data, we can generate some random inputs and test that the results
    fall within the minimum and maximum bounds.
    """
    NUM_YEARS = 9999
    MIN_SOURCES, MAX_SOURCES = 0, 99
    MIN_MASS, MAX_MASS = 0, 9999
    MIN_C, MAX_C = 0.1, 0.5
    MIN_N, MAX_N = 0.001, 0.01
    MIN_LIG, MAX_LIG = 0.01, 0.1

    min_c_input = MIN_MASS * MIN_C * MIN_SOURCES
    max_c_input = MAX_MASS * MAX_C * MAX_SOURCES

    def generate_random_carbon_sources():
        return [
            CarbonSource(
                mass=random.uniform(MIN_MASS, MAX_MASS),
                carbon_content=random.uniform(MIN_C, MAX_C),
                nitrogen_content=random.uniform(MIN_N, MAX_N),
                lignin_content=random.uniform(MIN_LIG, MAX_LIG)
            ) for _ in range(0, random.randint(MIN_SOURCES, MAX_SOURCES))
        ]

    timestamps = list(range(0, NUM_YEARS))
    annual_carbon_sources = [
        generate_random_carbon_sources() for _ in timestamps
    ]

    result = _run_annual_organic_carbon_inputs(
        timestamps,
        annual_carbon_sources
    )

    for i in range(0, NUM_YEARS):
        assert result.timestamps[i] == timestamps[i]
        assert min_c_input <= result.organic_carbon_inputs[i] <= max_c_input
        assert MIN_N <= result.average_nitrogen_contents[i] <= MAX_N
        assert MIN_LIG <= result.average_lignin_contents[i] <= MAX_LIG


@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
@patch(f"{class_path}.related_cycles")
def test_run_tier_2_with_generalised_monthly_measurements(mock_related_cycles, *args):
    """
    Test for sites with monthly climate measurements (e.g., `precipitationMonthly`) with dates in the format `--MM`.

    Tier 2 model should not run, as monthly climate measurements must be associated with a year and a month in the
    format `YYYY-MM`. Therefore, `run` function is expected to return an empty list `[]`.
    """

    SUBFOLDER = TIER_2_SUBFOLDERS[0]
    folder = f"{fixtures_folder}/{SUBFOLDER}"

    mock_related_cycles.return_value = _load_cycles(f"{folder}/cycles.jsonld")

    with open(f"{folder}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    result = run(site)
    assert result == []


@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
@patch(f"{class_path}.related_cycles")
def test_run_tier_2_with_incomplete_climate_data(mock_related_cycles, *args):

    SUBFOLDER = TIER_2_SUBFOLDERS[1]
    folder = f"{fixtures_folder}/{SUBFOLDER}"

    mock_related_cycles.return_value = _load_cycles(f"{folder}/cycles.jsonld")

    with open(f"{folder}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    result = run(site)
    assert result == []


@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
@patch(f"{class_path}.related_cycles")
def test_run_tier_2_with_initial_soc(mock_related_cycles, *args):

    SUBFOLDER = TIER_2_SUBFOLDERS[2]
    folder = f"{fixtures_folder}/{SUBFOLDER}"

    mock_related_cycles.return_value = _load_cycles(f"{folder}/cycles.jsonld")

    with open(f"{folder}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    with open(f"{folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(site)
    assert result == expected


@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
@patch(f"{class_path}.related_cycles")
def test_run_tier_2_with_multi_year_cycles(mock_related_cycles, *args):

    SUBFOLDER = TIER_2_SUBFOLDERS[3]
    folder = f"{fixtures_folder}/{SUBFOLDER}"

    mock_related_cycles.return_value = _load_cycles(f"{folder}/cycles.jsonld")

    with open(f"{folder}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    with open(f"{folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(site)
    assert result == expected


@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
@patch(f"{class_path}.related_cycles")
def test_run_tier_2_without_any_measurements(mock_related_cycles, *args):

    SUBFOLDER = TIER_2_SUBFOLDERS[4]
    folder = f"{fixtures_folder}/{SUBFOLDER}"

    mock_related_cycles.return_value = _load_cycles(f"{folder}/cycles.jsonld")

    with open(f"{folder}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    with open(f"{folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(site)
    assert result == expected


@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
@patch(f"{class_path}.related_cycles")
def test_run_tier_2_without_initial_soc(mock_related_cycles, *args):

    SUBFOLDER = TIER_2_SUBFOLDERS[5]
    folder = f"{fixtures_folder}/{SUBFOLDER}"

    mock_related_cycles.return_value = _load_cycles(f"{folder}/cycles.jsonld")

    with open(f"{folder}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    with open(f"{folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(site)
    assert result == expected
