# pre-commit-hooks
| Hook ID         | Description |
|:--------------:|:-----|
| [`pydantic-to-json`](#pydantic-to-json) |  Convert instanciated pydantic models to their corresponding JSON representation |
| [`pydantic-to-schema`](#pydantic-to-schema)      |  Convert pydantic model declarations to corresponding JSON schemas | 

## Pydantic hooks
[![Pydantic v1](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json)](https://docs.pydantic.dev/1.10/contributing/#badges)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
[![versions](https://img.shields.io/pypi/pyversions/pydantic.svg)](https://github.com/pydantic/pydantic)
[![license](https://img.shields.io/github/license/pydantic/pydantic.svg)](https://github.com/pydantic/pydantic/blob/main/LICENSE)

Hooks which handle the exportation of Pydantic models.


For example ...
```python
from pydantic import BaseModel

class ExampleClass(BaseModel):
  x: int

example_instance = ExampleClass(x=2)
```
Would export to ...
<table>
<tr>
<th> example_instance.json<br>(<a href="#pydantic-to-json">pydantic-to-json</a>) </th>
<th> ExampleClass.json<br>(<a href="#pydantic-to-schema">pydantic-to-schema</a>)  </th>
</tr>
<tr>
<td>
  
```json
{
  "x": 2
}
```

</td>
<td>

```json
{
  "properties": {
    "x": {
      "title": "X",
      "type": "integer"
    }
  },
  "required": [
    "x"
  ],
  "title": "ExampleClass",
  "type": "object"
}
```

</td>
</tr>
</table>


### pydantic-to-json

[![Pydantic v1](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json)](https://docs.pydantic.dev/1.10/contributing/#badges)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
[![versions](https://img.shields.io/pypi/pyversions/pydantic.svg)](https://github.com/pydantic/pydantic)
[![license](https://img.shields.io/github/license/pydantic/pydantic.svg)](https://github.com/pydantic/pydantic/blob/main/LICENSE)

A [pre-commit](https://pre-commit.com/) hook to convert _**instanciated**_ [pydantic](https://docs.pydantic.dev/latest/) classes to their respective JSON information dumps.

> By default, only the Pydantic models located within changed files are exported;<br>this behavior is overridable using both/either `input` and `all`

Minimal usage: 
```
repos:
  - repo: https://github.com/Mermeid-Designs/pre-commit-hooks
    rev: ""  # can specify specific revision if needed
    hooks:
    - id: pydantic-to-json
      args:
        [
          "--output",
          "path/to/output/folder",
        ]
```

Parameters:
- `output` ($\color{red}Required$): `str`, path to the desired folder where you would like the exported `JSON dictionaries` to be stored. If the folder does not exist, it will be created. Any existing JSONs will be overwritten, if applicable.
- `input` ($Optional$): `str`, absolute or relative path to a Python package, sub-package, or module that contains the Pydantic model class declaration(s) you wish to export. The `input` may reference files outside the scope of the repo invoking this pre-commit call.
- `all` ($Optional$): flag denoting all Pydantic model class declaration(s) within `input` shall be exported, (not just ones within changed files).
  
Output: Naming convention is as follows `{YourClassName}.json`

> 📌 **NOTE**:
>
> - _**ALL**_ Pydantic model class declaration(s) within `input` can potentially be exported, regardless of if they are normally visible to `input` (e.g. private class declarations)
> - `--all` is necessary if `input` references files outside the scope of the repo invoking this pre-commit call

### pydantic-to-schema

[![Pydantic v1](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json)](https://docs.pydantic.dev/1.10/contributing/#badges)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)
[![versions](https://img.shields.io/pypi/pyversions/pydantic.svg)](https://github.com/pydantic/pydantic)
[![license](https://img.shields.io/github/license/pydantic/pydantic.svg)](https://github.com/pydantic/pydantic/blob/main/LICENSE)

A [pre-commit](https://pre-commit.com/) hook to convert [pydantic](https://docs.pydantic.dev/latest/) _**class declarations**_ to their respective JSON schemas

> By default, only the Pydantic models located within changed files are exported;<br>this behavior is overridable using both/either `input` and `all`

Minimal usage: 
```
repos:
  - repo: https://github.com/Mermeid-Designs/pre-commit-hooks
    rev: ""  # can specify specific revision if needed
    hooks:
    - id: pydantic-to-schema
      args:
        [
          "--output",
          "path/to/output/folder",
        ]
```

Parameters:
- `output` ($\color{red}Required$): `str`, path to the desired folder where you would like the exported `JSON dictionaries` to be stored. If the folder does not exist, it will be created. Any existing JSONs will be overwritten, if applicable.
- `input` ($Optional$): `str`, absolute or relative path to a Python package, sub-package, or module that contains the Pydantic model class declaration(s) you wish to export. The `input` may reference files outside the scope of the repo invoking this pre-commit call.
- `all` ($Optional$): flag denoting all Pydantic model class declaration(s) within `input` shall be exported, (not just ones within changed files).
  
Output: Naming convention is as follows `{YourClassName}.json`

> 📌 **NOTE**:
>
> - _**ALL**_ Pydantic model class declaration(s) within `input` can potentially be exported, regardless of if they are normally visible to `input` (e.g. private class declarations)
> - `--all` is necessary if `input` references files outside the scope of the repo invoking this pre-commit call
