from typing import Dict, Union, List, Tuple
import sys
from pathlib import Path

from loguru import logger

from .schema_validation import GeoJsonLint
from .geometry_utils import (
    input_to_geojson,
    any_geojson_to_featurecollection,
)
from .validation_utils import (
    VALIDATION_CRITERIA,
    check_criteria,
    process_validation,
)
from .fix_utils import process_fix

logger.remove()
logger_format = "{time:YYYY-MM-DD_HH:mm:ss.SSS} | {message}"
logger.add(sink=sys.stderr, format=logger_format, level="INFO")


def validate_schema(geojson_input) -> Tuple[bool, Union[str, None]]:
    """
    Returns (True, None) if the input geojson conforms to the geojson json schema v7,
    and (False, "reason") if not.
    Enhances error messages by specifying which elements failed validation.
    """
    geojson_data = input_to_geojson(geojson_input)
    errors = GeoJsonLint().lint(geojson_data)
    return errors


def validate_geometries(
    geojson_input: Union[dict, str, Path],
    criteria_invalid: List[str] = VALIDATION_CRITERIA["invalid"],
    criteria_problematic: List[str] = VALIDATION_CRITERIA["problematic"],
) -> Dict:
    """
    Validate that a GeoJSON conforms to the geojson specs.

    Args:
        geojson: Input GeoJSON FeatureCollection, Feature, Geometry or filepath to (Geo)JSON/file.
        criteria_invalid: A list of validation criteria that are invalid according the GeoJSON specification.
        criteria_problematic: A list of validation criteria that are valid, but problematic with some tools.

    Returns:
        The validated & fixed GeoJSON feature collection.
    """
    if not criteria_invalid and not criteria_problematic:
        raise ValueError(
            "Select at least one criteria in `criteria_invalid` or `criteria_problematic`"
        )
    check_criteria(criteria_invalid, criteria_type="invalid")
    check_criteria(criteria_problematic, criteria_type="problematic")

    geojson_input = input_to_geojson(geojson_input)
    fc = any_geojson_to_featurecollection(geojson_input)

    geometries = [feature["geometry"] for feature in fc["features"]]
    # TODO: Could extract geometries here and use as input as before.
    results = process_validation(geometries, criteria_invalid, criteria_problematic)

    if criteria_invalid and "crs_defined" in criteria_invalid and "crs" in fc:
        results["invalid"]["crs_defined"] = True
        # "old-style crs member is not recommended, this object should be removed"

    logger.info(f"Validation results: {results}")
    return results


def fix_geometries(geojson_input):
    criteria_to_fix = [
        "unclosed",
        "duplicate_nodes",
        "exterior_not_ccw",
        "interior_not_cw",
    ]
    results = validate_geometries(
        geojson_input, criteria_invalid=criteria_to_fix, criteria_problematic=None
    )
    # TODO: Reptition from validate, same task twice. Output from validation? even validate schema here?
    geojson_input = input_to_geojson(geojson_input)
    validate_schema(geojson_input)
    fc = any_geojson_to_featurecollection(geojson_input)

    # Apply results and fix.
    fixed_fc = process_fix(
        fc, results, criteria_to_fix
    )  # TODO: check if the original fc was edited
    return fixed_fc
