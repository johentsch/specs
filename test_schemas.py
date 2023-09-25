
import argparse
import json
from typing import Sequence, TypeAlias

from jsonschema import validate
from jsonschema.exceptions import ValidationError


parser = argparse.ArgumentParser(
                    description='Validate json format.')

parser.add_argument('-f', '--file', action='append', default=['chor001.measuremap.json'],
                    help="validate measure map (%(default)s)")

parser.add_argument('-v', '--verbose', action="store_true",
                    help="verbose output")

Measure: TypeAlias = dict
MeasureMap: TypeAlias = Sequence[Measure]

def load_json(path):
    if not 'schema' in path:
        print('<==', path)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_measure(measure: Measure, measure_schema=None):
    if not measure_schema:
        measure_schema = load_json('measure.schema.json')
    validate(measure, measure_schema)

def test_measure_from_scratch():
    measure = {
        "count": 1,
        "number": 1,
        "time_signature": "3/4",
        "qstamp": 0.0,
        "nominal_length": 3.0,
        "actual_length": 1.0,
        "start_repeat": False,
        "end_repeat": False,
        "next": [
            2,
        ]
    }
    validate_measure(measure)
    measure["next"] = ["2"]
    try:
        validate_measure(measure)
        raise AssertionError(f"Validation of {measure} should have failed because ID is not present.")
    except ValidationError:
        pass
    measure["ID"] = "1"
    validate_measure(measure)

def test_measures_from_map(measure_map: MeasureMap):
    measure_schema = load_json('measure.schema.json')
    for measure in measure_map:
        try:
            validate_measure(measure, measure_schema)
        except ValidationError as e:
            print(f"Validation of {measure} failed with:\n{e!r}")

def validate_measure_map_file(filepath: str):
    measure_map = load_json(filepath)
    measure_map_schema = load_json('map.schema.json')
    validate(measure_map, measure_map_schema)

if __name__ == '__main__':
    args = parser.parse_args()

    test_measure_from_scratch()

    for f in args.file:
        print('test_measures_from_map...')
        measure_map = load_json(f)
        test_measures_from_map(measure_map)

        print('validate_measure_map_file...')
        validate_measure_map_file(f)

        print()