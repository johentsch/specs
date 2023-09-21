# MeasureMap specification

Currently the specification consists of two JSONschemas:

* `measure.schema.json`: the fields that a single measure map entry may have
* `map.schema.json`: in its current form, it's simply an array of `Measure` objects, but it could be extended to 
  include, for example, a `version` field.

The separation gives us flexibility in terms of various JSONschemas we might want to define for different types of 
measure maps. For example, the current `map.schema.json` is equivalent to 
[JSON lines format](https://www.atatus.com/glossary/jsonl/), adding a `version` field could be separate schema, 
incompatible with JSONL.