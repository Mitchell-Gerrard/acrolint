# acrolint

A linting tool for acronyms (project scaffold).

## Development

Create a virtual environment and install dev requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Run formatting and linting:

```bash
pre-commit run --all-files
``` 

Run tests:

```bash
pytest
```

Build and publish (after tagging a release):

```bash
python -m build
python -m twine upload dist/*
```

On GitHub Actions, set the `PYPI_API_TOKEN` secret to publish automatically when pushing a tag `v*`.
