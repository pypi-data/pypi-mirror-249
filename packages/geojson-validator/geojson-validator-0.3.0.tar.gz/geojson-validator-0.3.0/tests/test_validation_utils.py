import pytest

from .context import validation_utils


def test_check_criteria_invalid():
    with pytest.raises(ValueError):
        validation_utils.check_criteria(["non_existent_criteria"], "invalid")


def test_check_criteria_valid():
    try:
        validation_utils.check_criteria(["unclosed", "duplicate_nodes"], "invalid")
        validation_utils.check_criteria(["holes"], "problematic")
    except ValueError:
        pytest.fail("Unexpected ValueError for valid criteria")


def test_process_validation_valid_polygon_without_criteria():
    geometries = [
        {"type": "Polygon", "coordinates": [[[0, 0], [1, 1], [1, 0], [0, 0]]]}
    ]
    results = validation_utils.process_validation(geometries, [], [])
    assert not results["invalid"]
    assert not results["problematic"]


def test_process_validation_invalid_geometry():
    # unclosed
    geometries = [
        {"type": "Polygon", "coordinates": [[[0, 0], [1, 1], [1, 0]]]}
    ]  # Missing closing point
    invalid_criteria = ["unclosed"]
    results = validation_utils.process_validation(geometries, invalid_criteria, [])
    assert "unclosed" in results["invalid"]


def test_process_validation_error_no_type():
    # Test handling of geometry missing the 'type' field
    geometries = [{"coordinates": [[[0, 0], [1, 1], [1, 0], [0, 0]]]}]  # No type field
    with pytest.raises(ValueError):
        validation_utils.process_validation(geometries, [], [])


def test_process_validation_multiple_types():
    # Second geometry in Multipolygon and third geometry is unclosed
    geometries = [
        {"type": "Polygon", "coordinates": [[[0, 0], [1, 1], [1, 0], [0, 0]]]},
        {
            "type": "MultiPolygon",
            "coordinates": [
                [[[0, 0], [2, 2], [2, 0], [0, 0]]],
                [[[0, 0], [2, 2], [2, 0], [0, 1]]],  # invalid
                [[[0, 0], [1, 1], [1, 0]]],  # invalid
            ],
        },
        {"type": "Polygon", "coordinates": [[[0, 0], [1, 1], [1, 0]]]},
    ]
    invalid_criteria = ["unclosed"]
    results = validation_utils.process_validation(geometries, invalid_criteria, [])
    assert results["invalid"]["unclosed"] == [{1: [1, 2]}, 2]
    assert results["count_geometry_types"] == {"Polygon": 2, "MultiPolygon": 1}
