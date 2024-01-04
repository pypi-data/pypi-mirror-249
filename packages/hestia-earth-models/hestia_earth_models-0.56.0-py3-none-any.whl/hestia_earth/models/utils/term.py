from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.api import find_node, search

from ..log import debugMissingLookup
from .constant import Units

LIMIT = 1000


def get_lookup_value(lookup_term: dict, column: str, skip_debug: bool = False, **kwargs):
    table_name = f"{lookup_term.get('termType')}.csv" if lookup_term else None
    value = get_table_value(
        download_lookup(table_name), 'termid', lookup_term.get('@id'), column_name(column)
    ) if table_name else None
    debugMissingLookup(
        table_name, 'termid', lookup_term.get('@id'), column, value, **kwargs
    ) if lookup_term and not skip_debug else None
    return value


def get_liquid_fuel_terms():
    """
    Find all "liquid" `fuel` terms from the Glossary:
    - https://hestia.earth/glossary?termType=fuel&query=gasoline
    - https://hestia.earth/glossary?termType=fuel&query=petrol
    - https://hestia.earth/glossary?termType=fuel&query=diesel

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.FUEL.value
                    }
                }
            ],
            "should": [
                {
                    "regexp": {
                        "name": "gasoline*"
                    }
                },
                {
                    "regexp": {
                        "name": "petrol*"
                    }
                },
                {
                    "regexp": {
                        "name": "diesel*"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_wood_fuel_terms():
    """
    Find all "wood" `fuel` terms from the Glossary that have a `Energy content (lower heating value)` property:
    - https://hestia.earth/glossary?termType=fuel&query=wood

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.FUEL.value
                    }
                },
                {
                    "nested": {
                        "path": "defaultProperties",
                        "query": {
                            "match": {
                                "defaultProperties.term.name.keyword": "Energy content (lower heating value)"
                            }
                        }
                    }
                }
            ],
            "should": [
                {
                    "regexp": {
                        "name": "wood*"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_irrigation_terms():
    """
    Find all `water` terms from the Glossary:
    https://hestia.earth/glossary?termType=water

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = find_node(SchemaType.TERM, {
        'termType.keyword': TermTermType.WATER.value
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_urea_terms():
    """
    Find all `inorganicFertiliser` urea terms from the Glossary:
    https://hestia.earth/glossary?termType=inorganicFertiliser&query=urea

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = find_node(SchemaType.TERM, {
        'termType.keyword': TermTermType.INORGANICFERTILISER.value,
        'name': 'urea'
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_excreta_N_terms():
    """
    Find all `excreta` terms in `kg N` from the Glossary:
    https://hestia.earth/glossary?termType=excreta

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = find_node(SchemaType.TERM, {
        'termType.keyword': TermTermType.EXCRETA.value,
        'units.keyword': Units.KG_N.value
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_excreta_VS_terms():
    """
    Find all `excreta` terms in `kg Vs` from the Glossary:
    https://hestia.earth/glossary?termType=excreta

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = find_node(SchemaType.TERM, {
        'termType.keyword': TermTermType.EXCRETA.value,
        'units.keyword': Units.KG_VS.value
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_tillage_terms():
    """
    Find all `landUseManagement` terms of "tillage" from the Glossary:
    https://hestia.earth/glossary?termType=tillage&query=tillage

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = find_node(SchemaType.TERM, {
        'termType.keyword': TermTermType.TILLAGE.value,
        'name': 'tillage'
    }, limit=LIMIT)
    return [n['@id'] for n in terms if 'depth' not in n['@id'].lower()]


def get_generic_crop():
    terms = find_node(SchemaType.TERM, {
        'termType.keyword': TermTermType.CROP.value,
        'name': 'Generic crop seed'
    }, limit=1)
    return terms[0] if len(terms) > 0 else None


def get_rice_paddy_terms():
    """
    Find all `crop` terms of "rice paddy" from the Glossary:
    https://hestia.earth/glossary?termType=crop&query=rice%20paddy

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType": TermTermType.CROP.value
                    }
                },
                {
                    "regexp": {
                        "name": "rice*"
                    }
                },
                {
                    "regexp": {
                        "name": "flooded*"
                    }
                }
            ]
        }
    }, limit=LIMIT)
    return [n['@id'] for n in terms if 'depth' not in n['@id'].lower()]


def get_crop_residue_terms():
    terms = find_node(SchemaType.TERM, {'termType.keyword': TermTermType.CROPRESIDUE.value}, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_digestible_energy_terms():
    """
    Find all "digestible energy" `property` terms from the Glossary:
    https://hestia.earth/glossary?termType=property&query=digestible%20energy

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.PROPERTY.value
                    }
                }
            ],
            "should": [
                {
                    "match_phrase_prefix": {
                        "name": "Digestible energy"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_energy_digestibility_terms():
    """
    Find all "energy digestibility" `property` terms from the Glossary:
    https://hestia.earth/glossary?termType=property&query=energy%digestibility

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.PROPERTY.value
                    }
                }
            ],
            "should": [
                {
                    "match_phrase_prefix": {
                        "name": "Energy digestibility"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_crop_residue_management_terms():
    """
    Find all `cropResidueManagement` terms from the Glossary:
    https://hestia.earth/glossary?termType=cropResidueManagement

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.CROPRESIDUEMANAGEMENT.value
                    }
                }
            ]
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_all_emission_terms():
    """
    Find all `emission` terms from the Glossary:
    https://hestia.earth/glossary?termType=emission

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.EMISSION.value
                    }
                }
            ]
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_milkYield_terms():
    """
    Find all "milk yield" `animalManagement` terms from the Glossary:
    https://hestia.earth/glossary?query=milk%20yield&termType=animalManagement

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.ANIMALMANAGEMENT.value
                    }
                }
            ],
            "should": [
                {
                    "match_phrase_prefix": {
                        "name": "Milk yield"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))


def get_wool_terms():
    """
    Find all "wool" `animalProduct` terms from the Glossary:
    https://hestia.earth/glossary?query=wool&termType=animalProduct

    Returns
    -------
    list
        List of matching term `@id` as `str`.
    """
    terms = search({
        "bool": {
            "must": [
                {
                    "match": {
                        "@type": SchemaType.TERM.value
                    }
                },
                {
                    "match": {
                        "termType.keyword": TermTermType.ANIMALPRODUCT.value
                    }
                }
            ],
            "should": [
                {
                    "match_phrase_prefix": {
                        "name": "Wool"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }, limit=LIMIT)
    return list(map(lambda n: n['@id'], terms))
