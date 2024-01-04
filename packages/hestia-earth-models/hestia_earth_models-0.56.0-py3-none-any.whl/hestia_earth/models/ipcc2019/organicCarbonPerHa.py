"""
The IPCC Tier 2 model for estimating soil organic carbon stock changes in the 0 - 30cm depth interval for croplands
remaining croplands. Source:
[IPCC 2019, Vol. 4, Chapter 10](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch05_Cropland.pdf).

Currently, the Tier 2 implementation does not take into account the irrigation of cycles when estimating soil organic
carbon stock changes. This model is planned be extended to with an implementation of the the IPCC Tier 1 model.
"""
from enum import Enum
from pydash.objects import merge
from functools import reduce
from numpy import exp, mean
from typing import Any, NamedTuple, Union

from hestia_earth.schema import MeasurementMethodClassification, TermTermType
from hestia_earth.utils.date import diff_in_years
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import flatten, list_sum, non_empty_list

from hestia_earth.models.log import logShouldRun
from hestia_earth.models.utils.cycle import check_cycle_site_ids_identical, group_cycles_by_year
from hestia_earth.models.utils.measurement import (
    _new_measurement,
    group_measurement_values_by_year,
    most_relevant_measurement_value_by_depth_and_date
)
from hestia_earth.models.utils.property import get_node_property
from hestia_earth.models.utils.site import related_cycles
from hestia_earth.models.utils.term import get_lookup_value

from . import MODEL

REQUIREMENTS = {
    "Site": {
        "siteType": "cropland",
        "measurements": [
            {
                "@type": "Measurement",
                "value": "",
                "term.@id": "sandContent",
                "optional": {
                    "depthUpper": "0",
                    "depthLower": "30",
                    "dates": ""
                }
            },
            {"@type": "Measurement", "value": "", "dates": "", "term.@id": "temperatureMonthly"},
            {"@type": "Measurement", "value": "", "dates": "", "term.@id": "precipitationMonthly"},
            {"@type": "Measurement", "value": "", "dates": "", "term.@id": "potentialEvapotranspirationMonthly"}
        ],
        "optional": {
            "measurements": [
                {
                    "@type": "Measurement",
                    "value": "",
                    "dates": "",
                    "depthUpper": "0",
                    "depthLower": "30",
                    "term.@id": " organicCarbonPerHa"
                }
            ]
        },
        "related": {
            "Cycle": [{
                "@type": "Cycle",
                "endDate": "",
                "products": [
                    {
                        "@type": "Product",
                        "value": "",
                        "term.@id": [
                            "aboveGroundCropResidueLeftOnField",
                            "aboveGroundCropResidueIncorporated",
                            "belowGroundCropResidue"
                        ],
                        "properties": [
                            {
                                "@type": "Property",
                                "value": "",
                                "term.@id": ["carbonContent", "nitrogenContent", "ligninContent"]
                            }
                        ]
                    }
                ],
                "optional": {
                    "startDate": "",
                    "products": [
                        {
                            "@type": "Product",
                            "value": "",
                            "term.@id": [
                                "discardedCropLeftOnField",
                                "discardedCropIncorporated"
                            ],
                            "properties": [
                                {
                                    "@type": "Property",
                                    "value": "",
                                    "term.@id": ["carbonContent", "nitrogenContent", "ligninContent"]
                                }
                            ]
                        }
                    ],
                    "inputs": [
                        {
                            "@type": "Input",
                            "value": "",
                            "term.termType": [
                                "organicFertiliser",
                                "soilAmendment"
                            ],
                            "properties": [
                                {
                                    "@type": "Property",
                                    "value": "",
                                    "term.@id": ["carbonContent", "nitrogenContent", "ligninContent"]
                                }
                            ]
                        }
                    ],
                    "practices": [
                        {
                            "@type": "Practice",
                            "value": "",
                            "term.termType": "tillage"
                        },
                        {
                            "@type": "Practice",
                            "value": "",
                            "startDate": "",
                            "endDate": "",
                            "term": {
                                "@type": "Term",
                                "termType": "waterRegime",
                                "name": "irrigated"
                            }
                        }
                    ]
                }
            }]
        }
    }
}
LOOKUPS = {
    "tillage": "IPCC_TILLAGE_CATEGORY"
}
RETURNS = {
    "Measurement": [{
        "value": "",
        "dates": "",
        "depthUpper": "0",
        "depthLower": "30",
        "methodClassification": "tier 2 model"
    }]
}
TERM_ID = 'organicCarbonPerHa'

NUMBER_OF_TILLAGES_TERM_ID = 'numberOfTillages'
TEMPERATURE_MONTHLY_TERM_ID = 'temperatureMonthly'
PRECIPITATION_MONTHLY_TERM_ID = 'precipitationMonthly'
PET_MONTHLY_TERM_ID = 'potentialEvapotranspirationMonthly'
SAND_CONTENT_TERM_ID = 'sandContent'

CROP_RESIDUE_TERM_IDS = [
    'aboveGroundCropResidueIncorporated',
    'aboveGroundCropResidueLeftOnField',
    'discardedCropIncorporated',
    'discardedCropLeftOnField',
    'belowGroundCropResidue'
]

PROPERTY_TERM_IDS = [
    'carbonContent',
    'nitrogenContent',
    'ligninContent'
]

CARBON_SOURCE_TERM_TYPES = [
    TermTermType.ORGANICFERTILISER.value,
    TermTermType.SOILAMENDMENT.value,
    TermTermType.SEED.value
]

PERCENT_THRESHOLD = 30
DEPTH_UPPER = 0
DEPTH_LOWER = 30
MIN_RUN_IN_PERIOD = 5

DEFAULT_PARAMS = {
    "active_decay_factor": 7.4,
    "slow_decay_factor": 0.209,
    "passive_decay_factor": 0.00689,
    "f_1": 0.378,
    "f_2_full_tillage": 0.455,
    "f_2_reduced_tillage": 0.477,
    "f_2_no_tillage": 0.5,
    "f_2_unknown_tillage": 0.368,
    "f_3": 0.455,
    "f_5": 0.0855,
    "f_6": 0.0504,
    "f_7": 0.42,
    "f_8": 0.45,
    "tillage_factor_full_tillage": 3.036,
    "tillage_factor_reduced_tillage": 2.075,
    "tillage_factor_no_tillage": 1,
    "maximum_temperature": 45,
    "optimum_temperature": 33.69,
    "water_factor_slope": 1.331,
    "default_carbon_content": 0.42,
    "default_nitrogen_content": 0.0085,
    "default_lignin_content": 0.073
}


# --- FORMAT MEASUREMENT OUTPUT ---


def _measurement(year: int, value: float, method_classification: str) -> dict:
    """
    Build a Hestia `Measurement` node to contain a value calculated by the models.

    Parameters
    ----------
    year : int
        The year that the value is associated with.
    value : float
        The value calculated by either the Tier 1 or Tier 2 model.
    method_classification :str
        The method tier used to calculate the value, either `tier 1 model` or `tier 2 model`.

    Returns
    -------
    dict
        A valid Hestia `Measurement` node, see: https://www.hestia.earth/schema/Measurement.
    """
    measurement = _new_measurement(TERM_ID, MODEL)
    measurement['value'] = [value]
    measurement['dates'] = [f"{year}-12-31"]
    measurement['depthUpper'] = DEPTH_UPPER
    measurement['depthLower'] = DEPTH_LOWER
    measurement['methodClassification'] = method_classification
    return measurement


# --- IPCC MANAGEMENT CATEGORY ENUM ---


IpccManagementCategory = Enum(
    "IpccManagementCategory",
    [
        "FULL_TILLAGE",
        "REDUCED_TILLAGE",
        "NO_TILLAGE",
        "SEVERELY_DEGRADED",
        "IMPROVED_GRASSLAND",
        "HIGH_INTENSITY_GRAZING",
        "NOMINALLY_MANAGED",
        "OTHER",
    ],
)


# --- INNER KEY ENUM (FOR UTILITY) ---


_InnerKey = Enum(
    "_InnerKey",
    [
        "TEMPERATURES",
        "PRECIPITATIONS",
        "PETS",
        "IS_IRRIGATEDS",
        "CARBON_SOURCES",
        "TILLAGE_CATEGORY"
    ],
)


INNER_KEYS_RUN_WITH_IRRIGATION = [
    _InnerKey.TEMPERATURES,
    _InnerKey.PRECIPITATIONS,
    _InnerKey.PETS,
    _InnerKey.IS_IRRIGATEDS,
    _InnerKey.CARBON_SOURCES,
    _InnerKey.TILLAGE_CATEGORY,
]

INNER_KEYS_RUN_WITHOUT_IRRIGATION = [
    _InnerKey.TEMPERATURES,
    _InnerKey.PRECIPITATIONS,
    _InnerKey.PETS,
    _InnerKey.CARBON_SOURCES,
    _InnerKey.TILLAGE_CATEGORY,
]


# --- NAMED TUPLES FOR CARBON SOURCES AND MODEL RESULTS ---


CarbonSource = NamedTuple(
    "CarbonSource",
    [
        ("mass", float),
        ("carbon_content", float),
        ("nitrogen_content", float),
        ("lignin_content", float),
    ]
)
"""
A single carbon source (e.g. crop residues or organic amendment).

Attributes
-----------
mass : float
    The dry-matter mass of the carbon source, kg ha-1
carbon_content : float
    The carbon content of the carbon source, decimal proportion, kg C (kg d.m.)-1.
nitrogen_content : float
    The nitrogen content of the carbon source, decimal_proportion, kg N (kg d.m.)-1.
lignin_content : float
    The lignin content of the carbon source, decimal_proportion, kg lignin (kg d.m.)-1.
"""


TemperatureFactorResult = NamedTuple(
    "TemperatureFactorResult",
    [
        ("timestamps", list[float]),
        ("annual_temperature_factors", list[float])
    ]
)
"""
A named tuple to hold the result of `_run_annual_temperature_factors`.

Attributes
----------
timestamps : list[int]
    A list of integer timestamps (e.g. `[1995, 1996]`) for each year in the inventory.
annual_temperature_factors : list[float]
    A list of annual temperature factors for each year in the inventory, dimensionless, between `0` and `1`.
"""


WaterFactorResult = NamedTuple(
    "WaterFactorResult",
    [
        ("timestamps", list[float]),
        ("annual_water_factors", list[float])
    ]
)
"""
A named tuple to hold the result of `_run_annual_water_factors`.

Attributes
----------
timestamps : list[int]
    A list of integer timestamps (e.g. `[1995, 1996]`) for each year in the inventory.
annual_water_factors : list[float]
    A list of annual water factors for each year in the inventory, dimensionless, between `0.31935` and `2.25`.
"""


CarbonInputResult = NamedTuple(
    "CarbonInputResult",
    [
        ("timestamps", list[float]),
        ("organic_carbon_inputs", list[float]),
        ("average_nitrogen_contents", list[float]),
        ("average_lignin_contents", list[float]),
    ]
)
"""
A named tuple to hold the result of `_run_annual_organic_carbon_inputs`.

Attributes
----------
timestamps : list[int]
    A list of integer timestamps (e.g. `[1995, 1996]`) for each year in the inventory.
organic_carbon_inputs : list[float]
    A list of organic carbon inputs to the soil for each year in the inventory, kg C ha-1.
average_nitrogen_contents : list[float]
    A list of the average nitrogen contents of the carbon sources for each year in the inventory, decimal_proportion,
    kg N (kg d.m.)-1.
average_lignin_contents : list[float]
    A list of the average lignin contents of the carbon sources for each year in the inventory, decimal_proportion,
    kg lignin (kg d.m.)-1.
"""


Tier2SocResult = NamedTuple(
    "Tier2SocResult",
    [
        ("timestamps", list[float]),
        ("active_pool_soc_stocks", list[float]),
        ("slow_pool_soc_stocks", list[float]),
        ("passive_pool_soc_stocks", list[float]),
    ]
)
"""
A named tuple to hold the result of `_run_soc_stocks`.

Attributes
----------
timestamps : list[int]
    A list of integer timestamps (e.g. `[1995, 1996]`) for each year in the inventory.
active_pool_soc_stocks : list[float]
    The active sub-pool SOC stock for each year in the inventory, kg C ha-1.
slow_pool_soc_stocks : list[float]
    The slow sub-pool SOC stock for each year in the inventory, kg C ha-1.
passive_pool_soc_stocks : list[float]
    The passive sub-pool SOC stock for each year in the inventory, kg C ha-1.
"""


# --- IPCC MANAGEMENT CATEGORY DECISION TREES ---


IPCC_TILLAGE_MANAGEMENT_CATEGORY_TO_LOOKUP_VALUES = {
    IpccManagementCategory.FULL_TILLAGE: 'Full tillage',
    IpccManagementCategory.REDUCED_TILLAGE: 'Reduced tillage',
    IpccManagementCategory.NO_TILLAGE: 'No tillage'
}
"""
Mappings from `IpccManagementCategory` to 'IPCC_TILLAGE_MANAGEMENT_CATEGORY' lookup values for tillage practices.
"""


def _check_zero_tillages(practices: list[dict]) -> bool:
    """
    Checks whether a list of `Practice`s nodes describe 0 total tillages, or not.

    Parameters
    ----------
    practices : list[dict]
        A list of Hestia `Practice` nodes, see: https://www.hestia.earth/schema/Practice.

    Returns
    -------
    bool
        Whether or not 0 tillages counted.
    """
    practice = find_term_match(practices, NUMBER_OF_TILLAGES_TERM_ID)
    nTillages = list_sum(practice.get('value', []))
    return nTillages <= 0


def _check_cycle_tillage_management_category(
    cycle: dict,
    ipcc_tillage_management_category: IpccManagementCategory
) -> bool:
    """
    Checks whether a Hesita `Cycle` node meets the requirements of a specific tillage `IpccManagementCategory`.

    Parameters
    ----------
    cycle : dict
        A Hestia `Cycle` node, see: https://www.hestia.earth/schema/Cycle.
    ipcc_tillage_management_category : IpccManagementCategory)
        The `IpccManagementCategory` to match.

    Returns
    -------
    bool
        Whether or not the cycle meets the requirements for the category.
    """
    lookup = LOOKUPS["tillage"]
    target_lookup_value = (
        IPCC_TILLAGE_MANAGEMENT_CATEGORY_TO_LOOKUP_VALUES.get(ipcc_tillage_management_category, None)
    )

    practices = cycle.get('practices', [])
    tillage_practices = list(filter(lambda practice: get_lookup_value(
        practice.get('term', {}), lookup) == target_lookup_value, practices))

    values = flatten([practice.get('value', []) for practice in tillage_practices])

    return (
        list_sum(values) > PERCENT_THRESHOLD and _check_zero_tillages(practices)
        if ipcc_tillage_management_category == IpccManagementCategory.NO_TILLAGE
        else list_sum(values) > PERCENT_THRESHOLD
    )


TILLAGE_MANAGEMENT_CATEGORY_DECISION_TREE = {
    IpccManagementCategory.FULL_TILLAGE: (
        lambda cycles, key: any(_check_cycle_tillage_management_category(cycle, key) for cycle in cycles)
    ),
    IpccManagementCategory.REDUCED_TILLAGE: (
        lambda cycles, key: any(_check_cycle_tillage_management_category(cycle, key) for cycle in cycles)
    ),
    IpccManagementCategory.NO_TILLAGE: (
        lambda cycles, key: any(_check_cycle_tillage_management_category(cycle, key) for cycle in cycles)
    )
}


def _assign_ipcc_tillage_category(
    cycles: list[dict],
    default: IpccManagementCategory = IpccManagementCategory.FULL_TILLAGE
) -> IpccManagementCategory:
    """
    Assigns a tillage `IpccManagementCategory` to a list of Hestia `Cycle`s.

    Parameters
    ----------
    cycles : list[dict])
        A list of Hestia `Cycle` nodes, see: https://www.hestia.earth/schema/Cycle.

    Returns
    -------
        IpccManagementCategory: The assigned tillage `IpccManagementCategory`.
    """
    return next(
        (
            key for key in TILLAGE_MANAGEMENT_CATEGORY_DECISION_TREE
            if TILLAGE_MANAGEMENT_CATEGORY_DECISION_TREE[key](cycles, key)
        ),
        default
    ) if len(cycles) > 0 else default


# --- TIER 2: ANNUAL TEMPERATURE FACTOR FROM MONTHLY TEMPERATURE DATA ---


def _calc_temperature_factor(
    average_temperature: float,
    maximum_temperature: float = 45.0,
    optimum_temperature: float = 33.69,
) -> float:
    """
    Equation 5.0E, part 2. Calculate the temperature effect on decomposition in mineral soils for a single month using
    the Steady-State Method.

    If `average_temperature >= maximum_temperature` the function should always return 0.

    Parameters
    ----------
    average_temperature : float
        The average air temperature of a given month, degrees C.
    maximum_temperature : float
        The maximum air temperature for decomposition, degrees C, default value: `45.0`.
    optimum_temperature : float
        The optimum air temperature for decomposition, degrees C, default value: `33.69`.

    Returns
    -------
    float
        The air temperature effect on decomposition for a given month, dimensionless, between `0` and `1`.
    """
    prelim = (maximum_temperature - average_temperature) / (
        maximum_temperature - optimum_temperature
    )
    return 0 if average_temperature >= maximum_temperature else (
        pow(prelim, 0.2) * exp((0.2 / 2.63) * (1 - pow(prelim, 2.63)))
    )


def _calc_annual_temperature_factor(
    average_temperature_monthly: list[float],
    maximum_temperature: float = 45.0,
    optimum_temperature: float = 33.69,
) -> Union[float, None]:
    """
    Equation 5.0E, part 1. Calculate the average annual temperature effect on decomposition in mineral soils using the
    Steady-State Method.

    Parameters
    ----------
    average_temperature_monthly : list[float]
        A list of monthly average air temperatures in degrees C, must have a length of 12.

    Returns
    -------
    float | None
        Average annual temperature factor, dimensionless, between `0` and `1`, or `None` if the input list is empty.
    """
    return mean(
        list(
            _calc_temperature_factor(t, maximum_temperature, optimum_temperature)
            for t in average_temperature_monthly
        )
    ) if average_temperature_monthly else None


# --- TIER 2: ANNUAL WATER FACTOR FROM MONTHLY PRECIPITATION, POTENTIAL EVAPOTRANSPIRATION AND IRRIGATION DATA ---


def _calc_water_factor(
    precipitation: float,
    pet: float,
    is_irrigated: bool = False,
    water_factor_slope: float = 1.331,
) -> float:
    """
    Equation 5.0F, part 2. Calculate the water effect on decomposition in mineral soils for a single month using the
    Steady-State Method.

    If `is_irrigated == True` the function should always return `0.775`.

    Parameters
    ----------
    precipitation : float
        The sum total precipitation of a given month, mm.
    pet : float
        The sum total potential evapotranspiration in a given month, mm.
    is_irrigated : bool
        Whether or not irrigation has been used in a given month.
    water_factor_slope : float
        The slope for mappet term to estimate water factor, dimensionless, default value: `1.331`.

    Returns
    -------
    float
        The water effect on decomposition for a given month, dimensionless, between `0.2129` and `1.5`.
    """
    mappet = min(1.25, precipitation / pet)
    return 0.775 if is_irrigated else 0.2129 + (water_factor_slope * (mappet)) - (0.2413 * pow(mappet, 2))


def _calc_annual_water_factor(
    precipitation_monthly: list[float],
    pet_monthly: list[float],
    is_irrigated_monthly: Union[list[bool], None] = None,
    water_factor_slope: float = 1.331,
) -> Union[float, None]:
    """
    Equation 5.0F, part 1. Calculate the average annual water effect on decomposition in mineral soils using the
    Steady-State Method multiplied by a coefficient of `1.5`.

    Parameters
    ----------
    precipitation_monthly : list[float]
        A list of monthly sum total precipitation values in mm, must have a length of 12.
    pet_monthly : list[float])
        A list of monthly sum total potential evapotranspiration values in mm, must have a length of 12.
    is_irrigated_monthly : list[boolean] | None)
        A list of true/false values that describe whether irrigation has been used in each calendar month, must have a
        length of 12. If `None` is provided, a list of 12 `False` values is used.
    water_factor_slope : float
        The slope for mappet term to estimate water factor, dimensionless, default value: `1.331`.

    Returns
    -------
    float | None
        Average annual water factor multiplied by `1.5`, dimensionless, between `0.31935` and `2.25`,
        or `None` if any of the input lists are empty.
    """
    is_irrigated_monthly = (
        [False] * 12 if is_irrigated_monthly is None else is_irrigated_monthly
    )
    zipped = zip(precipitation_monthly, pet_monthly, is_irrigated_monthly)
    return 1.5 * mean(list(
        _calc_water_factor(precipitation, pet, is_irrigated, water_factor_slope)
        for precipitation, pet, is_irrigated in zipped
    )) if all([precipitation_monthly, pet_monthly]) else None


# --- TIER 2: ANNUAL TOTAL ORGANIC CARBON INPUT TO SOIL, NITROGEN CONTENT AND LIGNIN CONTENT FROM CARBON SOURCES ---

def _calc_total_organic_carbon_input(
    carbon_sources: list[CarbonSource], default_carbon_content=0.42
) -> float:
    """
    Equation 5.0H part 1. Calculate the total organic carbon to a site from all carbon sources (above-ground and
    below-ground crop residues, organic amendments, etc.).

    Parameters
    ----------
    carbon_sources : list[CarbonSource])
        A list of carbon sources as named tuples with the format
        `(mass: float, carbon_content: float, nitrogen_content: float, lignin_content: float)`.
    default_carbon_content : float
        The default carbon content of a carbon source, decimal proportion, kg C (kg d.m.)-1.

    Returns
    -------
    float
        The total mass of organic carbon inputted into the site, kg C ha-1.
    """
    return sum(c.mass * (c.carbon_content if c.carbon_content else default_carbon_content) for c in carbon_sources)


def _calc_average_nitrogen_content_of_organic_carbon_sources(
    carbon_sources: list[CarbonSource], default_nitrogen_content=0.0085
) -> float:
    """
    Calculate the average nitrogen content of the carbon inputs through a weighted mean.

    Parameters
    ----------
    carbon_sources : list[CarbonSource]
        A list of carbon sources as named tuples with the format
        `(mass: float, carbon_content: float, nitrogen_content: float, lignin_content: float)`
    default_nitrogen_content : float
        The default nitrogen content of a carbon source, decimal proportion, kg N (kg d.m.)-1.

    Returns
    -------
    float
        The average nitrogen content of the carbon sources, decimal_proportion, kg N (kg d.m.)-1.
    """
    total_weight = sum(c.mass for c in carbon_sources)
    weighted_values = [
        c.mass * (c.nitrogen_content if c.nitrogen_content else default_nitrogen_content) for c in carbon_sources
    ]
    return sum(weighted_values) / total_weight if total_weight > 0 else default_nitrogen_content


def _calc_average_lignin_content_of_organic_carbon_sources(
    carbon_sources: list[dict[str, float]], default_lignin_content=0.073
) -> float:
    """
    Calculate the average lignin content of the carbon inputs through a weighted mean.

    Parameters
    ----------
    carbon_sources : list[CarbonSource]
        A list of carbon sources as named tuples with the format
        `(mass: float, carbon_content: float, nitrogen_content: float, lignin_content: float)`
    default_lignin_content : float
        The default lignin content of a carbon source, decimal proportion, kg lignin (kg d.m.)-1.

    Returns
    -------
    float
        The average lignin content of the carbon sources, decimal_proportion, kg lignin (kg d.m.)-1.
    """
    total_weight = sum(c.mass for c in carbon_sources)
    weighted_values = [
        c.mass * (c.lignin_content if c.lignin_content else default_lignin_content) for c in carbon_sources
    ]
    return sum(weighted_values) / total_weight if total_weight > 0 else default_lignin_content


# --- TIER 2: ACTIVE SUB-POOL SOC STOCK ---


def _calc_beta(
    carbon_input: float,
    lignin_content: float = 0.073,
    nitrogen_content: float = 0.0083,
) -> float:
    """
    Equation 5.0G, part 2. Calculate the C input to the metabolic dead organic matter C component, kg C ha-1.

    See table 5.5b for default values for lignin content and nitrogen content.

    Parameters
    ----------
    carbon_input : float
        Total carbon input to the soil during an inventory year, kg C ha-1.
    lignin_content : float
        The average lignin content of carbon input sources, decimal proportion, default value: `0.073`.
    nitrogen_content : float
        The average nitrogen content of carbon sources, decimal proportion, default value: `0.0083`.

    Returns
    -------
    float
        The C input to the metabolic dead organic matter C component, kg C ha-1.
    """
    return carbon_input * (0.85 - 0.018 * (lignin_content / nitrogen_content))


def _get_f_2(
    tillage_management_category: IpccManagementCategory = IpccManagementCategory.OTHER,
    f_2_full_tillage: float = 0.455,
    f_2_reduced_tillage: float = 0.477,
    f_2_no_tillage: float = 0.5,
    f_2_unknown_tillage: float = 0.368,
) -> float:
    """
    Get the value of `f_2` (the stabilisation efficiencies for structural decay products entering the active pool)
    based on the tillage `IpccManagementCategory`.

    If tillage regime is unknown, `IpccManagementCategory.OTHER` should be assumed.

    Parameters
    ----------
    tillage_management_category : (IpccManagementCategory)
        The tillage category of the inventory year, default value: `IpccManagementCategory.OTHER`.
    f_2_full_tillage : float
        The stabilisation efficiencies for structural decay products entering the active pool under full tillage,
        decimal proportion, default value: `0.455`.
    f_2_reduced_tillage : float
        The stabilisation efficiencies for structural decay products entering the active pool under reduced tillage,
        decimal proportion, default value: `0.477`.
    f_2_no_tillage : float
        The stabilisation efficiencies for structural decay products entering the active pool under no tillage,
        decimal proportion, default value: `0.5`.
    f_2_unknown_tillage : float
        The stabilisation efficiencies for structural decay products entering the active pool if tillage is not known,
        decimal proportion, default value: `0.368`.

    Returns
    -------
        float: The stabilisation efficiencies for structural decay products entering the active pool,
        decimal proportion.
    """
    ipcc_tillage_management_category_to_f_2s = {
        IpccManagementCategory.FULL_TILLAGE: f_2_full_tillage,
        IpccManagementCategory.REDUCED_TILLAGE: f_2_reduced_tillage,
        IpccManagementCategory.NO_TILLAGE: f_2_no_tillage,
        IpccManagementCategory.OTHER: f_2_unknown_tillage
    }
    default = f_2_unknown_tillage

    return ipcc_tillage_management_category_to_f_2s.get(tillage_management_category, default)


def _calc_f_4(sand_content: float = 0.33, f_5: float = 0.0855) -> float:
    """
    Equation 5.0C, part 4. Calculate the value of the stabilisation efficiencies for active pool decay products
    entering the slow pool based on the sand content of the soil.

    Parameters
    ----------
    sand_content : float)
        The sand content of the soil, decimal proportion, default value: `0.33`.
    f_5 : float
        The stabilisation efficiencies for active pool decay products entering the passive pool, decimal_proportion,
        default value: `0.0855`.

    Returns
    -------
    float
        The stabilisation efficiencies for active pool decay products entering the slow pool, decimal proportion.
    """
    return 1 - f_5 - (0.17 + 0.68 * sand_content)


def _calc_alpha(
    carbon_input: float,
    f_2: float,
    f_4: float,
    lignin_content: float = 0.073,
    nitrogen_content: float = 0.0083,
    f_1: float = 0.378,
    f_3: float = 0.455,
    f_5: float = 0.0855,
    f_6: float = 0.0504,
    f_7: float = 0.42,
    f_8: float = 0.45,
) -> float:
    """
    Equation 5.0G, part 1. Calculate the C input to the active soil carbon sub-pool, kg C ha-1.

    See table 5.5b for default values for lignin content and nitrogen content.

    Parameters
    ----------
    carbon_input : float
        Total carbon input to the soil during an inventory year, kg C ha-1.
    f_2 : float
        The stabilisation efficiencies for structural decay products entering the active pool, decimal proportion.
    f_4 : float
        The stabilisation efficiencies for active pool decay products entering the slow pool, decimal proportion.
    lignin_content : float
        The average lignin content of carbon input sources, decimal proportion, default value: `0.073`.
    nitrogen_content : float
        The average nitrogen content of carbon input sources, decimal proportion, default value: `0.0083`.
    sand_content : float
        The sand content of the soil, decimal proportion, default value: `0.33`.
    f_1 : float
        The stabilisation efficiencies for metabolic decay products entering the active pool, decimal proportion,
        default value: `0.378`.
    f_3 : float
        The stabilisation efficiencies for structural decay products entering the slow pool, decimal proportion,
        default value: `0.455`.
    f_5 : float
        The stabilisation efficiencies for active pool decay products entering the passive pool, decimal proportion,
        default value: `0.0855`.
    f_6 : float
        The stabilisation efficiencies for slow pool decay products entering the passive pool, decimal proportion,
        default value: `0.0504`.
    f_7 : float
        The stabilisation efficiencies for slow pool decay products entering the active pool, decimal proportion,
        default value: `0.42`.
    f_8 : float
        The stabilisation efficiencies for passive pool decay products entering the active pool, decimal proportion,
        default value: `0.45`.

    Returns
    -------
    float
        The C input to the active soil carbon sub-pool, kg C ha-1.
    """
    beta = _calc_beta(
        carbon_input, lignin_content=lignin_content, nitrogen_content=nitrogen_content
    )

    x = beta * f_1
    y = (carbon_input * (1 - lignin_content) - beta) * f_2
    z = (carbon_input * lignin_content) * f_3 * (f_7 + (f_6 * f_8))
    d = 1 - (f_4 * f_7) - (f_5 * f_8) - (f_4 * f_6 * f_8)
    return (x + y + z) / d


def _get_tillage_factor(
    tillage_management_category: IpccManagementCategory = IpccManagementCategory.FULL_TILLAGE,
    tillage_factor_full_tillage: float = 3.036,
    tillage_factor_reduced_tillage: float = 2.075,
    tillage_factor_no_tillage: float = 1,
) -> float:
    """
    Calculate the tillage disturbance modifier on decay rate for active and slow sub-pools based on the tillage
    `IpccManagementCategory`.

    If tillage regime is unknown, `FULL_TILLAGE` should be assumed.

    Parameters
    ----------
    tillage_factor_full_tillage : float)
        The tillage disturbance modifier for decay rates under full tillage, dimensionless, default value: `3.036`.
    tillage_factor_reduced_tillage : float
        Tillage disturbance modifier for decay rates under reduced tillage, dimensionless, default value: `2.075`.
    tillage_factor_no_tillage : float
        Tillage disturbance modifier for decay rates under no tillage, dimensionless, default value: `1`.

    Returns
    -------
    float
        The tillage disturbance modifier on decay rate for active and slow sub-pools, dimensionless.
    """
    ipcc_tillage_management_category_to_tillage_factors = {
        IpccManagementCategory.FULL_TILLAGE: tillage_factor_full_tillage,
        IpccManagementCategory.REDUCED_TILLAGE: tillage_factor_reduced_tillage,
        IpccManagementCategory.NO_TILLAGE: tillage_factor_no_tillage,
    }
    default = tillage_factor_full_tillage

    return ipcc_tillage_management_category_to_tillage_factors.get(
        tillage_management_category, default
    )


def _calc_active_pool_decay_rate(
    annual_temperature_factor: float,
    annual_water_factor: float,
    tillage_factor: float,
    sand_content: float = 0.33,
    active_decay_factor: float = 7.4,
) -> float:
    """
    Equation 5.0B, part 3. Calculate the decay rate for the active SOC sub-pool given conditions in an inventory year.

    Parameters
    ----------
    annual_temperature_factor : float
        Average annual temperature factor, dimensionless, between `0` and `1`.
    annual_water_factor : float
        Average annual water factor, dimensionless, between `0.31935` and `2.25`.
    tillage_factor : float
        The tillage disturbance modifier on decay rate for active and slow sub-pools, dimensionless.
    sand_content : float
        sand_content (float): The sand content of the soil, decimal proportion, default value: `0.33`.
    active_decay_factor : float
        decay rate constant under optimal conditions for decomposition of the active SOC subpool, year-1, default value:
        `7.4`.

    Returns
    -------
    float
        The decay rate for active SOC sub-pool, year-1.
    """
    sand_factor = 0.25 + (0.75 * sand_content)
    return (
        annual_temperature_factor
        * annual_water_factor
        * tillage_factor
        * sand_factor
        * active_decay_factor
    )


def _calc_active_pool_steady_state(
    alpha: float, active_pool_decay_rate: float
) -> float:
    """
    Equation 5.0B part 2. Calculate the steady state active sub-pool SOC stock given conditions in an inventory year.

    Parameters
    ----------
    alpha : float
        The C input to the active soil carbon sub-pool, kg C ha-1.
    active_pool_decay_rate : float
        Decay rate for active SOC sub-pool, year-1.

    Returns
    -------
    float
        The steady state active sub-pool SOC stock given conditions in year y, kg C ha-1
    """
    return alpha / active_pool_decay_rate


# --- TIER 2: SLOW SUB-POOL SOC STOCK ---


def _calc_slow_pool_decay_rate(
    annual_temperature_factor: float,
    annual_water_factor: float,
    tillage_factor: float,
    slow_decay_factor: float = 0.209,
) -> float:
    """
    Equation 5.0C, part 3. Calculate the decay rate for the slow SOC sub-pool given conditions in an inventory year.

    Parameters
    ----------
    annual_temperature_factor : float
        Average annual temperature factor, dimensionless, between `0` and `1`.
    annual_water_factor : float
        Average annual water factor, dimensionless, between `0.31935` and `2.25`.
    tillage_factor : float
        The tillage disturbance modifier on decay rate for active and slow sub-pools, dimensionless.
    slow_decay_factor : float)
        The decay rate constant under optimal conditions for decomposition of the slow SOC subpool, year-1,
        default value: `0.209`.

    Returns
    -------
    float
        The decay rate for slow SOC sub-pool, year-1.
    """
    return (
        annual_temperature_factor
        * annual_water_factor
        * tillage_factor
        * slow_decay_factor
    )


def _calc_slow_pool_steady_state(
    carbon_input: float,
    f_4: float,
    active_pool_steady_state: float,
    active_pool_decay_rate: float,
    slow_pool_decay_rate: float,
    lignin_content: float = 0.073,
    f_3: float = 0.455,
) -> float:
    """
    Equation 5.0C, part 2. Calculate the steady state slow sub-pool SOC stock given conditions in an inventory year.

    Parameters
    ----------
    carbon_input : float
        Total carbon input to the soil during an inventory year, kg C ha-1.
    f_4 : float
        The stabilisation efficiencies for active pool decay products entering the slow pool, decimal proportion.
    active_pool_steady_state : float
        The steady state active sub-pool SOC stock given conditions in year y, kg C ha-1
    active_pool_decay_rate : float
        Decay rate for active SOC sub-pool, year-1.
    slow_pool_decay_rate : float
        Decay rate for slow SOC sub-pool, year-1.
    lignin_content : float
        The average lignin content of carbon input sources, decimal proportion, default value: `0.073`.
    f_3 : float
        The stabilisation efficiencies for structural decay products entering the slow pool, decimal proportion,
        default value: `0.455`.

    Returns
    -------
    float
        The steady state slow sub-pool SOC stock given conditions in year y, kg C ha-1
    """
    x = carbon_input * lignin_content * f_3
    y = active_pool_steady_state * active_pool_decay_rate * f_4
    return (x + y) / slow_pool_decay_rate


# --- TIER 2: PASSIVE SUB-POOL SOC STOCK ---


def _calc_passive_pool_decay_rate(
    annual_temperature_factor: float,
    annual_water_factor: float,
    passive_decay_factor: float = 0.00689,
) -> float:
    """
    Equation 5.0D, part 3. Calculate the decay rate for the passive SOC sub-pool given conditions in an inventory year.

    Parameters
    ----------
    annual_temperature_factor : float
        Average annual temperature factor, dimensionless, between `0` and `1`.
    annual_water_factor : float
        Average annual water factor, dimensionless, between `0.31935` and `2.25`.
    passive_decay_factor : float
        decay rate constant under optimal conditions for decomposition of the passive SOC subpool, year-1,
        default value: `0.00689`.

    Returns
    -------
    float
        The decay rate for passive SOC sub-pool, year-1.
    """
    return annual_temperature_factor * annual_water_factor * passive_decay_factor


def _calc_passive_pool_steady_state(
    active_pool_steady_state: float,
    slow_pool_steady_state: float,
    active_pool_decay_rate: float,
    slow_pool_decay_rate: float,
    passive_pool_decay_rate: float,
    f_5: float = 0.0855,
    f_6: float = 0.0504,
) -> float:
    """
    Equation 5.0D, part 2. Calculate the steady state passive sub-pool SOC stock given conditions in an inventory year.

    Parameters
    ----------
    active_pool_steady_state : float
        The steady state active sub-pool SOC stock given conditions in year y, kg C ha-1.
    slow_pool_steady_state : float
        The steady state slow sub-pool SOC stock given conditions in year y, kg C ha-1.
    active_pool_decay_rate : float
        Decay rate for active SOC sub-pool, year-1.
    slow_pool_decay_rate : float
        Decay rate for slow SOC sub-pool, year-1.
    passive_pool_decay_rate : float
        Decay rate for passive SOC sub-pool, year-1.
    f_5 : float
        The stabilisation efficiencies for active pool decay products entering the passive pool, decimal proportion,
        default value: `0.0855`.
    f_6 : float
        The stabilisation efficiencies for slow pool decay products entering the passive pool, decimal proportion,
        default value: `0.0504`.

    Returns
    -------
    float
        The steady state passive sub-pool SOC stock given conditions in year y, kg C ha-1.
    """
    x = active_pool_steady_state * active_pool_decay_rate * f_5
    y = slow_pool_steady_state * slow_pool_decay_rate * f_6
    return (x + y) / passive_pool_decay_rate


# --- TIER 2:  GENERIC SUB-POOL SOC STOCK ---


def _calc_sub_pool_soc_stock(
    sub_pool_steady_state: (float),
    previous_sub_pool_soc_stock: (float),
    sub_pool_decay_rate: (float),
    timestep: int = 1,
) -> float:
    """
    Generalised from equations 5.0B, 5.0C and 5.0D, part 1. Calculate the sub-pool SOC stock in year y, kg C ha-1.

    If `sub_pool_decay_rate > 1` then set its value to `1` for this calculation.

    Parameters
    ----------
    sub_pool_steady_state : float
        The steady state sub-pool SOC stock given conditions in year y, kg C ha-1.
    previous_sub_pool_soc_stock : float
        The sub-pool SOC stock in year y-timestep (by default one year ago), kg C ha-1.
    sub_pool_decay_rate : float
        Decay rate for active SOC sub-pool, year-1.
    timestep : int
        The number of years between current and previous inventory year.

    Returns
    -------
    float
        The sub-pool SOC stock in year y, kg C ha-1.
    """
    sub_pool_decay_rate = min(1, sub_pool_decay_rate)
    return (
        previous_sub_pool_soc_stock
        + (sub_pool_steady_state - previous_sub_pool_soc_stock)
        * timestep
        * sub_pool_decay_rate
    )


# --- TIER 2: SOC STOCK CHANGE ---


def _calc_soc_stock(
    active_pool_soc_stock: float,
    slow_pool_soc_stock: float,
    passive_pool_soc_stock: float,
) -> float:
    """
    Equation 5.0A, part 3. Calculate the total SOC stock for a site by summing its active, slow and passive SOC stock
    sub-pools. This is the value we need for our `organicCarbonPerHa` measurement.

    Parameters
    ----------
    actve_pool_soc_stock : float
        The active sub-pool SOC stock in year y, kg C ha-1.
    slow_pool_soc_stock : float
        The slow sub-pool SOC stock in year y, kg C ha-1.
    passive_pool_soc_stock : float
        The passive sub-pool SOC stock in year y, kg C ha-1.

    Returns
    -------
    float
        The SOC stock of a site in year y, kg C ha-1.
    """
    return active_pool_soc_stock + slow_pool_soc_stock + passive_pool_soc_stock


# --- TIER 2: RUN ACTIVE, SLOW AND PASSIVE SOC STOCKS ---


def timeseries_to_inventory(timeseries_data: list[float], run_in_period: int):
    """
    Convert annual data to inventory data by averaging the values for the run-in period.

    Parameters
    ----------
    timeseries_data : list[float]
        The timeseries data to be reformatted.
    run_in_period : int
        The length of the run-in in years.

    Returns
    -------
    list[float]
        The inventory formatted data, where value 0 is the average of the run-in values.
    """
    return [mean(timeseries_data[0:run_in_period])] + timeseries_data[run_in_period:]


def _run_soc_stocks(
    timestamps: list[int],
    annual_temperature_factors: list[float],
    annual_water_factors: list[float],
    annual_organic_carbon_inputs: list[float],
    annual_average_nitrogen_contents_of_organic_carbon_sources: list[float],
    annual_average_lignin_contents_of_organic_carbon_sources: list[float],
    annual_tillage_categories: Union[list[IpccManagementCategory], None] = None,
    sand_content: float = 0.33,
    run_in_period: int = 5,
    initial_soc_stock: Union[float, None] = None,
    params: Union[dict[str, float], None] = None,
) -> Tier2SocResult:
    """
    Run the IPCC Tier 2 SOC model with precomputed `annual_temperature_factors`, `annual_water_factors`,
    `annual_organic_carbon_inputs`, `annual_average_nitrogen_contents_of_organic_carbon_sources`,
    `annual_average_lignin_contents_of_organic_carbon_sources`.

    Parameters
    ----------
    timestamps : list[int]
        A list of integer timestamps (e.g. `[1995, 1996]`) for each year in the inventory.
    annual_temperature_factors : list[float]
        A list of temperature factors for each year in the inventory, dimensionless (see Equation 5.0E).
    annual_water_factors : list[float]
        A list of water factors for each year in the inventory, dimensionless (see Equation 5.0F).
    annual_organic_carbon_inputs : list[float]
        A list of organic carbon inputs to the soil for each year in the inventory, kg C ha-1 year-1
        (see Equation 5.0H).
    annual_average_nitrogen_contents_of_organic_carbon_sources : list[float]
        A list of the average nitrogen contents of the organic carbon sources for each year in the inventory,
        decimal proportion.
    annual_average_lignin_contents_of_organic_carbon_sources : list[float]
        A list of the average lignin contents of the organic carbon sources for each year in the inventory,
        decimal proportion.
    annual_tillage_categories : list[IpccManagementCategory] | None
        A list of the site's `IpccManagementCategory`s for each year in the inventory.
    sand_content : float
        The sand content of the site, decimal proportion, default value: `0.33`.
    run_in_period : int
        The length of the run-in period in years, must be greater than or equal to 1, default value: `5`.
    initial_soc_stock : float | None
        The measured or pre-computed initial SOC stock at the end of the run-in period, kg C ha-1.
    params : dict[str: float] | None
        Overrides for the model parameters. If `None` only default parameters will be used.

    Returns
    -------
    Tier2SocResult
        Returns an annual inventory of organicCarbonPerHa data in the format
        `(timestamps: list[int], organicCarbonPerHa_values: list[float], active_pool_soc_stocks: list[float],
        slow_pool_soc_stocks: list[float], passive_pool_soc_stocks: list[float])`
    """

    # --- MERGE ANY USER-SET PARAMETERS WITH THE IPCC DEFAULTS ---

    params = DEFAULT_PARAMS | (params or {})

    # --- GET F4 ---

    f_4 = _calc_f_4(sand_content, f_5=params.get("f_5"))

    # --- GET ANNUAL DATA ---

    annual_f_2s = [
        _get_f_2(
            till,
            f_2_full_tillage=params.get("f_2_full_tillage"),
            f_2_reduced_tillage=params.get("f_2_reduced_tillage"),
            f_2_no_tillage=params.get("f_2_no_tillage"),
            f_2_unknown_tillage=params.get("f_2_unknown_tillage"),
        )
        for till in annual_tillage_categories
    ]

    annual_tillage_factors = [
        _get_tillage_factor(
            till,
            tillage_factor_full_tillage=params.get("tillage_factor_full_tillage"),
            tillage_factor_reduced_tillage=params.get("tillage_factor_reduced_tillage"),
            tillage_factor_no_tillage=params.get("tillage_factor_no_tillage"),
        )
        for till in annual_tillage_categories
    ]

    # --- SPLIT ANNUAL DATA INTO RUN-IN AND INVENTORY PERIODS ---

    inventory_temperature_factors = timeseries_to_inventory(
        annual_temperature_factors, run_in_period
    )
    inventory_water_factors = timeseries_to_inventory(
        annual_water_factors, run_in_period
    )
    inventory_carbon_inputs = timeseries_to_inventory(
        annual_organic_carbon_inputs, run_in_period
    )
    inventory_nitrogen_contents = timeseries_to_inventory(
        annual_average_nitrogen_contents_of_organic_carbon_sources, run_in_period
    )
    inventory_lignin_contents = timeseries_to_inventory(
        annual_average_lignin_contents_of_organic_carbon_sources, run_in_period
    )
    inventory_f_2s = timeseries_to_inventory(annual_f_2s, run_in_period)
    inventory_tillage_factors = timeseries_to_inventory(
        annual_tillage_factors, run_in_period
    )

    inventory_timestamps = timestamps[
        run_in_period - 1:
    ]  # The last year of the run-in should be the first year of the inventory

    # --- CALCULATE THE ACTIVE ACTIVE POOL STEADY STATES ---

    inventory_alphas = [
        _calc_alpha(
            carbon_input,
            f_2,
            f_4,
            lignin_content,
            nitrogen_content,
            f_1=params.get("f_1"),
            f_3=params.get("f_3"),
            f_5=params.get("f_5"),
            f_6=params.get("f_6"),
            f_7=params.get("f_7"),
            f_8=params.get("f_8"),
        )
        for carbon_input, f_2, lignin_content, nitrogen_content in zip(
            inventory_carbon_inputs,
            inventory_f_2s,
            inventory_lignin_contents,
            inventory_nitrogen_contents,
        )
    ]

    inventory_active_pool_decay_rates = [
        _calc_active_pool_decay_rate(
            temp_fac,
            water_fac,
            till_fac,
            sand_content,
            active_decay_factor=params.get("active_decay_factor"),
        )
        for temp_fac, water_fac, till_fac in zip(
            inventory_temperature_factors,
            inventory_water_factors,
            inventory_tillage_factors,
        )
    ]

    inventory_active_pool_steady_states = [
        _calc_active_pool_steady_state(alpha, active_decay_rate)
        for alpha, active_decay_rate in zip(
            inventory_alphas, inventory_active_pool_decay_rates
        )
    ]

    # --- CALCULATE THE SLOW POOL STEADY STATES ---

    inventory_slow_pool_decay_rates = [
        _calc_slow_pool_decay_rate(
            temp_fac, water_fac, till_fac, slow_decay_factor=params.get("slow_decay_factor")
        )
        for temp_fac, water_fac, till_fac in zip(
            inventory_temperature_factors,
            inventory_water_factors,
            inventory_tillage_factors,
        )
    ]

    inventory_slow_pool_steady_states = [
        _calc_slow_pool_steady_state(
            carbon_input,
            f_4,
            active_steady_state,
            active_decay_rate,
            slow_decay_rate,
            lignin_content,
            f_3=params.get("f_3"),
        )
        for carbon_input, active_steady_state, active_decay_rate, slow_decay_rate, lignin_content in zip(
            inventory_carbon_inputs,
            inventory_active_pool_steady_states,
            inventory_active_pool_decay_rates,
            inventory_slow_pool_decay_rates,
            inventory_lignin_contents,
        )
    ]

    # --- CALCULATE THE PASSIVE POOL STEADY STATES ---

    inventory_passive_pool_decay_rates = [
        _calc_passive_pool_decay_rate(
            temp_fac, water_fac, passive_decay_factor=params.get("passive_decay_factor")
        )
        for temp_fac, water_fac in zip(
            inventory_temperature_factors, inventory_water_factors
        )
    ]

    inventory_passive_pool_steady_states = [
        _calc_passive_pool_steady_state(
            active_steady_state,
            slow_steady_state,
            active_decay_rate,
            slow_decay_rate,
            passive_decay_rate,
            f_5=params.get("f_5"),
            f_6=params.get("f_6"),
        )
        for active_steady_state, slow_steady_state, active_decay_rate, slow_decay_rate, passive_decay_rate in zip(
            inventory_active_pool_steady_states,
            inventory_slow_pool_steady_states,
            inventory_active_pool_decay_rates,
            inventory_slow_pool_decay_rates,
            inventory_passive_pool_decay_rates,
        )
    ]

    # --- CALCULATE THE ACTIVE, SLOW AND PASSIVE SOC STOCKS ---

    init_total_steady_state = (
        inventory_active_pool_steady_states[0] +
        inventory_slow_pool_steady_states[0] + inventory_passive_pool_steady_states[0]
    )

    init_active_frac = inventory_active_pool_steady_states[0]/init_total_steady_state
    init_slow_frac = inventory_slow_pool_steady_states[0]/init_total_steady_state
    init_passive_frac = 1 - (init_active_frac + init_slow_frac)

    inventory_active_pool_soc_stocks = []
    inventory_slow_pool_soc_stocks = []
    inventory_passive_pool_soc_stocks = []

    should_calc_run_in = initial_soc_stock is None

    inventory_active_pool_soc_stocks.insert(
        0,
        inventory_active_pool_steady_states[0]
        if should_calc_run_in
        else init_active_frac * initial_soc_stock,
    )
    inventory_slow_pool_soc_stocks.insert(
        0,
        inventory_slow_pool_steady_states[0]
        if should_calc_run_in
        else init_slow_frac * initial_soc_stock,
    )
    inventory_passive_pool_soc_stocks.insert(
        0,
        inventory_passive_pool_steady_states[0]
        if should_calc_run_in
        else init_passive_frac * initial_soc_stock,
    )

    for index in range(1, len(inventory_timestamps), 1):
        inventory_active_pool_soc_stocks.insert(
            index,
            _calc_sub_pool_soc_stock(
                inventory_active_pool_steady_states[index],
                inventory_active_pool_soc_stocks[index - 1],
                inventory_active_pool_decay_rates[index],
            ),
        )
        inventory_slow_pool_soc_stocks.insert(
            index,
            _calc_sub_pool_soc_stock(
                inventory_slow_pool_steady_states[index],
                inventory_slow_pool_soc_stocks[index - 1],
                inventory_slow_pool_decay_rates[index],
            ),
        )
        inventory_passive_pool_soc_stocks.insert(
            index,
            _calc_sub_pool_soc_stock(
                inventory_passive_pool_steady_states[index],
                inventory_passive_pool_soc_stocks[index - 1],
                inventory_passive_pool_decay_rates[index],
            ),
        )

    # --- RETURN THE RESULT ---

    return Tier2SocResult(
        timestamps=inventory_timestamps,
        active_pool_soc_stocks=inventory_active_pool_soc_stocks,
        slow_pool_soc_stocks=inventory_slow_pool_soc_stocks,
        passive_pool_soc_stocks=inventory_passive_pool_soc_stocks,
    )


# --- SOME UTILITY FUNCTIONS FOR GROUPING AND EXTRACTING HESTIA NODE DATA ---


def _check_consecutive(ints: list[int]) -> bool:
    """
    Checks whether a list of integers are consecutive.

    Used to determine whether annualised data is complete from every year from beggining to end.

    Parameters
    ----------
    ints : list[int]
        A list of integer values.

    Returns
    -------
    bool
        Whether or not the list of integers is consecutive.
    """
    range_list = list(range(min(ints), max(ints)+1)) if ints else []
    return all(a == b for a, b in zip(ints, range_list))


def _check_12_months(inner_dict: dict, keys: set[Any]):
    """
    Checks whether an inner dict has 12 months of data for each of the required inner keys.

    Parameters
    ----------
    inner_dict : dict
        A dictionary representing one year in a timeseries for the Tier 2 model.
    keys : set[Any]
        The required inner keys.

    Returns
    -------
    bool
        Whether or not the inner dict satisfies the conditions.
    """
    return all(
        len(inner_dict.get(key, [])) == 12 for key in keys
    )


# --- SUB-MODEL ANNUAL TEMPERATURE FACTORS ---


def _should_run_annual_temperature_factors(
    site: dict
) -> tuple[bool, dict]:
    """
    Extracts, formats and checks data from the site node to determine whether or not to run the annual temperature
    factors model on a specific Hestia `Site`.

    Parameters
    ----------
    site : dict
        A Hestia `Site` node, see: https://www.hestia.earth/schema/Site.

    Returns
    -------
    tuple[bool, dict]
        `(should_run, grouped_data)`.
    """
    measurements = site.get('measurements', [])
    temperature_monthly = find_term_match(measurements, TEMPERATURE_MONTHLY_TERM_ID, {})

    grouped_data = group_measurement_values_by_year(
        temperature_monthly,
        inner_key=_InnerKey.TEMPERATURES,
        complete_years_only=True
    )

    should_run = all([
        all(
            _check_12_months(inner, {_InnerKey.TEMPERATURES})
            for inner in grouped_data.values()
        ),
        len(grouped_data.keys()) >= MIN_RUN_IN_PERIOD,
        _check_consecutive(grouped_data.keys())
    ])

    logShouldRun(site, MODEL, TERM_ID, should_run, sub_model="_run_annual_temperature_factors")
    return should_run, grouped_data


def _run_annual_temperature_factors(
    timestamps: list[int],
    temperatures: list[list[float]],
    maximum_temperature: float = 45.0,
    optimum_temperature: float = 33.69,
):
    """
    Parameters
    ----------
    timestamps : list[int]
        A list of integer timestamps (e.g. `[1995, 1996]`) for each year in the inventory.
    temperatures : list[list[float]])
        A list of monthly average temperatures for each year in the inventory
        (e.g. `[[10,10,10,20,25,15,15,10,10,10,5,5]]`).
    maximum_temperature : float
        The maximum air temperature for decomposition, degrees C, default value: `45.0`.
    optimum_temperature : float
        The optimum air temperature for decomposition, degrees C, default value: `33.69`.

    Returns
    -------
    TemperatureFactorResult
        An inventory of annual temperature factor data as a named tuple with the format
        `(timestamps: list[int], annual_temperature_factors: list[float])`.
    """
    return TemperatureFactorResult(
        timestamps=timestamps,
        annual_temperature_factors=[
            _calc_annual_temperature_factor(
                monthly_temperatures, maximum_temperature, optimum_temperature
            )
            for monthly_temperatures in temperatures
        ],
    )


# --- SUB-MODEL ANNUAL WATER FACTORS ---


def _should_run_annual_water_factors(
    site: dict,
    cycles: list[dict]
) -> tuple[bool, bool, dict]:
    """
    Extracts, formats and checks data from the site and cycle nodes to determine determine whether or not to run the
    annual water factors model on a specific Hestia `Site` and `Cycle`s.

    TO DO: Implement checks for monthly is_irrigateds from cycles.

    Parameters
    ----------
    site : dict
        A Hestia `Site` node, see: https://www.hestia.earth/schema/Site.
    cycles : list[dict]
        A list of Hestia `Cycle` nodes, see: https://www.hestia.earth/schema/Cycle.

    Returns
    -------
    tuple[bool, bool, dict]
        `(should_run, run_with_irrigation, grouped_data)`.
    """
    measurements = site.get('measurements', [])
    precipitation_monthly = find_term_match(measurements, PRECIPITATION_MONTHLY_TERM_ID, {})
    potential_evapotranspiration_monthly = find_term_match(measurements, PET_MONTHLY_TERM_ID, {})

    grouped_precipitations = group_measurement_values_by_year(
        precipitation_monthly,
        inner_key=_InnerKey.PRECIPITATIONS,
        complete_years_only=True
    )
    grouped_pets = group_measurement_values_by_year(
        potential_evapotranspiration_monthly,
        inner_key=_InnerKey.PETS,
        complete_years_only=True
    )

    is_irrigateds = None  # TO DO: IMPLEMENT IS_IRRIGATEDS SEARCH
    run_with_irrigation = False if is_irrigateds is None else True

    grouped_data = (
        merge(grouped_precipitations, grouped_pets) if is_irrigateds is None else reduce(
            merge, [grouped_precipitations, grouped_pets, is_irrigateds]
        )
    )

    should_run = all([
        all(
            _check_12_months(inner, {_InnerKey.PRECIPITATIONS, _InnerKey.PETS})
            for inner in grouped_data.values()
        ),
        not run_with_irrigation or all(
            _check_12_months(inner, {_InnerKey.IS_IRRIGATEDS})
            for inner in grouped_data.values()
        ),
        len(grouped_data.keys()) >= MIN_RUN_IN_PERIOD,
        _check_consecutive(grouped_data.keys()),
        check_cycle_site_ids_identical(cycles)
    ])

    logShouldRun(
        site,
        MODEL,
        TERM_ID,
        should_run,
        sub_model="_run_annual_water_factors",
        run_with_irrigation=run_with_irrigation
    )
    return should_run, run_with_irrigation, grouped_data


def _run_annual_water_factors(
    timestamps: list[int],
    precipitations: list[list[float]],
    pets: list[list[float]],
    is_irrigateds: Union[list[list[bool]], None] = None,
    water_factor_slope: float = 1.331,
):
    """
    Parameters
    ----------
    timestamps : list[int]
        A list of integer timestamps (e.g. `[1995, 1996...]`) for each year in the inventory.
    precipitations : list[list[float]]
        A list of monthly sum precipitations for each year in the inventory
        (e.g. `[[10,10,10,20,25,15,15,10,10,10,5,5]]`).
    pets list[list[float]]
        A list of monthly sum potential evapotransiprations for each year in the inventory.
    is_irrigateds list[list[bool]] | None
        A list of monthly booleans that describe whether irrigation is used in a particular calendar month for each
        year in the inventory.
    water_factor_slope : float
        The slope for mappet term to estimate water factor, dimensionless, default value: `1.331`.

    Returns
    -------
    WaterFactorResult
        An inventory of annual water factor data as a named tuple with the format
        `(timestamps: list[int], annual_water_factors: list[float])`.
    """
    is_irrigateds = [None] * len(timestamps) if is_irrigateds is None else is_irrigateds
    return WaterFactorResult(
        timestamps=timestamps,
        annual_water_factors=[
            _calc_annual_water_factor(
                monthly_precipitations,
                monthly_pets,
                monthly_is_irrigateds,
                water_factor_slope,
            )
            for monthly_precipitations, monthly_pets, monthly_is_irrigateds in zip(
                precipitations, pets, is_irrigateds
            )
        ],
    )


# --- SUB-MODEL ANNUAL ORGANIC CARBON INPUTS ---


def _iterate_carbon_source(node: dict) -> Union[CarbonSource, None]:
    """
    Validates whether a node is a valid carbon source and returns
    a `CarbonSource` named tuple if yes.

    Parameters
    ----------
    node : dict
        A Hestia `Product` or `Input` node, see: https://www.hestia.earth/schema/Product
        or https://www.hestia.earth/schema/Input.

    Returns
    -------
    CarbonSource | None
        A `CarbonSource` named tuple if the node is a carbon source with the required properties, else `None`.
    """
    term = node.get('term', {})
    mass = list_sum(node.get('value', []))
    carbon_content, nitrogen_content, lignin_content = (
        get_node_property(node, term_id).get('value', 0)/100 for term_id in PROPERTY_TERM_IDS
    )

    should_run = all([
        any([
            term.get('@id', None) in CROP_RESIDUE_TERM_IDS,
            term.get('termType') in CARBON_SOURCE_TERM_TYPES
        ]),
        mass > 0,
        0 < carbon_content <= 1,
        0 < nitrogen_content <= 1,
        0 < lignin_content <= 1
    ])

    return (
        CarbonSource(
            mass, carbon_content, nitrogen_content, lignin_content
        ) if should_run else None
    )


def _get_carbon_sources_from_cycles(cycles: dict) -> list[CarbonSource]:
    """
    Retrieves and formats all of the valid carbon sources from a list of cycles.

    Carbon sources can be either a Hestia `Product` node (e.g. crop residue) or `Input` node (e.g. organic amendment).

    Parameters
    ----------
    cycles : list[dict]
        A list of Hestia `Cycle` nodes, see: https://www.hestia.earth/schema/Cycle.

    Returns
    -------
    list[CarbonSource]
        A formatted list of `CarbonSource`s for the inputted `Cycle`s.
    """
    inputs_and_products = non_empty_list(flatten(
        [cycle.get('inputs', []) + cycle.get('products', []) for cycle in cycles]
    ))

    return non_empty_list([_iterate_carbon_source(node) for node in inputs_and_products])


def _should_run_annual_organic_carbon_inputs(
    site: dict,
    cycles: list[dict]
) -> tuple[bool, dict]:
    """
    Extracts, formats and checks data from the site node to determine whether or not to run the annual organic carbon
    inputs model on a specific set of Hestia `Cycle`s.

    Parameters
    ----------
    cycles : list[dict]
        A list of Hestia `Cycle` nodes, see: https://www.hestia.earth/schema/Cycle.

    Returns
    -------
    tuple[bool, dict]
        `(should_run, grouped_data)`.
    """
    grouped_cycles = group_cycles_by_year(cycles)
    grouped_data = {
        year: {
            _InnerKey.CARBON_SOURCES: _get_carbon_sources_from_cycles(_cycles)
        } for year, _cycles in grouped_cycles.items()
    }

    should_run = all([
        len(grouped_data.keys()) >= MIN_RUN_IN_PERIOD,
        _check_consecutive(grouped_data.keys()),
        check_cycle_site_ids_identical(cycles)
    ])

    logShouldRun(site, MODEL, TERM_ID, should_run, sub_model="_run_annual_organic_carbon_inputs")
    return should_run, grouped_data


def _run_annual_organic_carbon_inputs(
    timestamps: list[int],
    annual_carbon_sources: list[list[CarbonSource]],
    default_carbon_content: float = 0.42,
    default_nitrogen_content: float = 0.0085,
    default_lignin_content: float = 0.073,
):
    """
    Calculate the organic carbon input, average nitrogen content of carbon sources and average lignin content of carbon
    sources for each year of the inventory.

    `timestamps` and `annual_carbon_sources` must have the same length.

    Parameters
    ----------
    timestamps : list[int]
        A list of integer timestamps (e.g. `[1995, 1996]`) for each year in the inventory.
    annual_carbon_sources : list[list[CarbonSource]]
        A list of carbon sources for each year of the inventory, where each carbon source is a named tupled with the
        format `(mass: float, carbon_content: float, nitrogen_content: float, lignin_content: float)`
    default_carbon_content : float
        The default carbon content of a carbon source, decimal proportion, kg C (kg d.m.)-1, default value: `0.42`.
    default_nitrogen_content : float
        The default nitrogen content of a carbon source, decimal proportion, kg N (kg d.m.)-1, default value: `0.0085`.
    default_lignin_content : float)
        The default lignin content of a carbon source, decimal proportion, kg lignin (kg d.m.)-1,
        default value: `0.073`.

    Returns
    -------
    CarbonInputResult
        An inventory of annual carbon input data as a named tuple with the format
        `(timestamps: list[int], organic_carbon_inputs: list[float], average_nitrogen_contents: list[float],
        average_lignin_contents: list[float])`
    """
    return CarbonInputResult(
        timestamps=timestamps,
        organic_carbon_inputs=[
            _calc_total_organic_carbon_input(sources, default_carbon_content=default_carbon_content)
            for sources in annual_carbon_sources
        ],
        average_nitrogen_contents=[
            _calc_average_nitrogen_content_of_organic_carbon_sources(
                sources, default_nitrogen_content=default_nitrogen_content)
            for sources in annual_carbon_sources
        ],
        average_lignin_contents=[
            _calc_average_lignin_content_of_organic_carbon_sources(
                sources, default_lignin_content=default_lignin_content)
            for sources in annual_carbon_sources
        ],
    )


# --- TIER 2 SOC MODEL ---


def _should_run_tier_2(
    site: dict
) -> tuple:
    """
    Extracts, formats and checks data from the site and cycle nodes to determine
    determine whether or not to run the Tier 2 SOC model.

    Parameters
    ----------
    site : dict
        A Hestia `Site` node, see: https://www.hestia.earth/schema/Site.
    cycles : list[dict]
        A list of Hestia `Cycle` nodes, see: https://www.hestia.earth/schema/Cycle.

    Returns
    -------
    tuple
        `(should_run, timestamps, temperatures, precipitations, pets, carbon_sources, tillage_categories, sand_content,
        is_irrigateds, run_in_period, initial_soc_stock)`
    """
    cycles = related_cycles(site.get('@id'))

    should_run_t, grouped_temperature_data = _should_run_annual_temperature_factors(site)
    should_run_w, run_with_irrigation, grouped_water_data = _should_run_annual_water_factors(site, cycles)
    should_run_c, grouped_carbon_sources_data = _should_run_annual_organic_carbon_inputs(site, cycles)

    grouped_cycles = group_cycles_by_year(cycles)

    grouped_tillage_categories = {
        year: {
            _InnerKey.TILLAGE_CATEGORY: _assign_ipcc_tillage_category(_cycles, IpccManagementCategory.OTHER)
        } for year, _cycles in grouped_cycles.items()
    }

    # Combine all the grouped data into one dictionary
    grouped_data = reduce(merge, [grouped_temperature_data, grouped_water_data,
                          grouped_carbon_sources_data, grouped_tillage_categories])

    # Select the correct keys for data completeness based on `run_with_irrigation`
    keys = INNER_KEYS_RUN_WITH_IRRIGATION if run_with_irrigation else INNER_KEYS_RUN_WITHOUT_IRRIGATION

    # Filter out any incomplete years
    complete_data = dict(filter(
        lambda item: all([key in item[1].keys() for key in keys]),
        grouped_data.items()
    ))

    timestamps = list(complete_data)
    start_year = timestamps[0] if timestamps else 0
    end_year = timestamps[-1] if timestamps else 0

    measurements = site.get('measurements', [])

    sand_content_value, _ = most_relevant_measurement_value_by_depth_and_date(
        measurements,
        SAND_CONTENT_TERM_ID,
        f"{start_year}-12-31",
        DEPTH_UPPER,
        DEPTH_LOWER,
        depth_strict=False
    ) if timestamps else (None, None)
    sand_content = sand_content_value/100 if sand_content_value else None

    initial_soc_stock_value, initial_soc_stock_date = most_relevant_measurement_value_by_depth_and_date(
        measurements,
        TERM_ID,
        f"{end_year}-12-31",
        DEPTH_UPPER,
        DEPTH_LOWER,
        depth_strict=True
    ) if timestamps else (None, None)

    run_with_initial_soc_stock = bool(initial_soc_stock_value and initial_soc_stock_date)

    run_in_period = (
        int(abs(diff_in_years(f"{start_year}-12-31", initial_soc_stock_date)) + 1)
        if run_with_initial_soc_stock else MIN_RUN_IN_PERIOD
    ) if timestamps else 0

    timestamps = list(complete_data.keys())
    temperatures = [complete_data[year][_InnerKey.TEMPERATURES] for year in timestamps]
    precipitations = [complete_data[year][_InnerKey.PRECIPITATIONS] for year in timestamps]
    pets = [complete_data[year][_InnerKey.PETS] for year in timestamps]
    annual_carbon_sources = [complete_data[year][_InnerKey.CARBON_SOURCES] for year in timestamps]
    annual_tillage_categories = [complete_data[year][_InnerKey.TILLAGE_CATEGORY] for year in timestamps]
    is_irrigateds = (
        [complete_data[year][_InnerKey.IS_IRRIGATEDS] for year in timestamps] if run_with_irrigation else None
    )

    should_run = all([
        should_run_t,
        should_run_w,
        should_run_c,
        sand_content is not None and 0 < sand_content <= 1,
        run_in_period >= MIN_RUN_IN_PERIOD,
        len(timestamps) >= run_in_period,
        check_cycle_site_ids_identical(cycles),
        _check_consecutive(timestamps)
    ])

    logShouldRun(
        site,
        MODEL,
        TERM_ID,
        should_run,
        sub_model="_run_tier_2",
        run_with_irrigation=run_with_irrigation,
        run_with_initial_soc_stock=run_with_initial_soc_stock,
        run_in_period=run_in_period
    )

    return (
        should_run,
        timestamps,
        temperatures,
        precipitations,
        pets,
        annual_carbon_sources,
        annual_tillage_categories,
        sand_content,
        is_irrigateds,
        run_in_period,
        initial_soc_stock_value
    )


def _run_tier_2(
    timestamps: list[int],
    temperatures: list[list[float]],
    precipitations: list[list[float]],
    pets: list[list[float]],
    annual_carbon_sources: list[list[CarbonSource]],
    annual_tillage_categories: list[IpccManagementCategory],
    sand_content: float = 0.33,
    is_irrigateds: Union[list[list[bool]], None] = None,
    run_in_period: int = 5,
    initial_soc_stock: Union[float, None] = None,
    params: Union[dict[str, float], None] = None,
) -> list[dict]:
    """
    Run the IPCC Tier 2 SOC model on a time series of annual data about a site and the mangagement activities taking
    place on it. `timestamps` and `annual_`... lists must be the same length.

    Parameters
    ----------
    timestamps : list[int]
        A list of integer timestamps (e.g. [1995, 1996...]) for each year in the inventory.
    temperatures : list[list[float]]
        A list of monthly average temperatures for each year in the inventory.
    precipitations : list[list[float]]
        A list of monthly sum precipitations for each year in the inventory.
    pets : list[list[float]]
        A list of monthly sum potential evapotransiprations for each year in the inventory.
    annual_carbon_sources : list[list[CarbonSource]]
        A list of carbon sources for each year of the inventory, where each carbon source is a named tupled with the
        format `(mass: float, carbon_content: float, nitrogen_content: float, lignin_content: float)`
    annual_tillage_categories : list[IpccManagementCategory)
        A list of the site's IpccManagementCategory for each year in the inventory.
    sand_content : float
        The sand content of the site, decimal proportion, default value: `0.33`.
    is_irrigateds : list[list[bool]] | None
        A list of monthly booleans that describe whether irrigation is used in a particular calendar month for each
        year in the inventory.
    run_in_period : int
        The length of the run-in period in years, must be greater than or equal to 1, default value: `5`.
    initial_soc_stock : float | None]
        The measured or pre-computed initial SOC stock at the end of the run-in period, kg C ha-1.
    params : dict | None
        Overrides for the model parameters. If `None` only default parameters will be used.

    Returns
    -------
    list[dict]
        A list of Hestia `Measurement` nodes containing the calculated SOC stocks and additional relevant data.
    """

    # --- MERGE ANY USER-SET PARAMETERS WITH THE IPCC DEFAULTS ---

    params = DEFAULT_PARAMS | (params or {})

    # --- COMPUTE FACTORS AND CARBON INPUTS ---

    _, annual_temperature_factors = _run_annual_temperature_factors(
        timestamps,
        temperatures,
        maximum_temperature=params.get('maximum_temperature'),
        optimum_temperature=params.get('optimum_temperature')
    )

    _, annual_water_factors = _run_annual_water_factors(
        timestamps,
        precipitations,
        pets,
        is_irrigateds,
        water_factor_slope=params.get('water_factor_slope')
    )

    (
        _,
        annual_organic_carbon_inputs,
        annual_nitrogen_contents,
        annual_lignin_contents
    ) = _run_annual_organic_carbon_inputs(
        timestamps,
        annual_carbon_sources,
        default_carbon_content=params.get('default_carbon_content'),
        default_nitrogen_content=params.get('default_nitrogen_content'),
        default_lignin_content=params.get('default_lignin_content')
    )

    # --- RUN THE MODEL ---

    result = _run_soc_stocks(
        timestamps=timestamps,
        annual_temperature_factors=annual_temperature_factors,
        annual_water_factors=annual_water_factors,
        annual_organic_carbon_inputs=annual_organic_carbon_inputs,
        annual_average_nitrogen_contents_of_organic_carbon_sources=annual_nitrogen_contents,
        annual_average_lignin_contents_of_organic_carbon_sources=annual_lignin_contents,
        annual_tillage_categories=annual_tillage_categories,
        sand_content=sand_content,
        run_in_period=run_in_period,
        initial_soc_stock=initial_soc_stock,
        params=params
    )

    values = [
        _calc_soc_stock(
            active,
            slow,
            passive
        ) for active, slow, passive in zip(
            result.active_pool_soc_stocks,
            result.slow_pool_soc_stocks,
            result.passive_pool_soc_stocks
        )
    ]

    # --- RETURN MEASUREMENT NODES ---

    return [
        _measurement(
            year,
            value,
            MeasurementMethodClassification.TIER_2_MODEL.value
        ) for year, value in zip(
            result.timestamps,
            values
        )
    ]


def run(site: dict) -> list[dict]:
    """
    Check which Tier of IPCC SOC model to run, run it and return the formatted output.

    TO DO: Implement Tier 1 model and uncomment relevant sections.

    Parameters
    ----------
    site : dict
        A Hestia `Site` node, see: https://www.hestia.earth/schema/Site.

    Returns
    -------
    list[dict]
        A list of Hestia `Measurement` nodes containing the calculated SOC stocks and additional relevant data.
    """
    should_run_tier_2, *tier_2_args = _should_run_tier_2(site)
    return _run_tier_2(*tier_2_args) if should_run_tier_2 else []
