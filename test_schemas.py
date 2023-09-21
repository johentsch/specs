import json
from typing import Sequence, TypeAlias

from jsonschema import validate
from jsonschema.exceptions import ValidationError

Measure: TypeAlias = dict
MeasureMap: TypeAlias = Sequence[Measure]

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_measure(measure: Measure):
    measure_schema = load_json('measure.schema.json')
    validate(measure, measure_schema)

def test_measure_from_scratch():
    measure = {
        "count": 1,
        "number": 1,
        "time-signature": "3\/4",
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

def test_measures_from_map(measure_map: MeasureMap):
    for measure in measure_map:
        try:
            validate_measure(measure)
        except ValidationError as e:
            print(f"Validation of {measure} failed with:\n{e!r}")

def validate_measure_map_file(filepath: str):
    measure_map = load_json(filepath)
    measure_map_schema = load_json('map.schema.json')
    validate(measure_map, measure_map_schema)

if __name__ == '__main__':
    test_measure_from_scratch()
    filepath = "chor001.measuremap.json"
    measure_map = load_json(filepath)
    test_measures_from_map(measure_map)
