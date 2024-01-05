<div align="center">

![PyPI - Version](https://img.shields.io/pypi/v/xai-explainer)
![PyPI - Downloads](https://img.shields.io/pypi/dm/xai-explainer)
![PyPI - License](https://img.shields.io/pypi/l/xai-explainer?color=brightgreen)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/xai-explainer)

</div>

# Installation

All stable versions can be installed from [PyPI] by using [pip] or your favorite package manager

    pip install xai-explainer

# Development

**Requirements:**
- Python 3.8 or higher
- [poetry] 1.2 or higher
- [make]

For installing the development environment run

```bash
make setup
```

Configure poetry for vscode
```bash
poetry config virtualenvs.in-project true
poetry install # or alternatively: "make setup"
```

Run scripts using poetry
```bash
poetry run python script_name.py
```

[make]: https://www.gnu.org/software/make/
[pip]: https://pypi.org/project/pip/
[poetry]: https://python-poetry.org/
[pypi]: https://pypi.org/