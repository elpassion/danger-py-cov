# danger-py-cov

The plugin parses the `.xml` coverage report and visualizes how the pull request affects the results. 

<h3 align="center">
  <a href="https://www.elpassion.com">
    <img src="/assets/readme/elpassion.png" alt="Find your EL Passion"/>
  </a>
</h3>


## Example output

### Current coverage is `100.00%`

| Files changed | Coverage | - |
| ------------- | -------- | --- |
| calculations.py | `100.00%` | :white_check_mark: |
| cobertura.py | `100.00%` | :white_check_mark: |
| models.py | `100.00%` | :white_check_mark: |
| plugin.py | `100.00%` | :white_check_mark: |
| report.py | `100.00%` | :white_check_mark: |

## Usage

Run the tests using the runner that supports XML reporting. For [pytest](https://docs.pytest.org/en/latest/) and [pytest-cov](https://pypi.org/project/pytest-cov/) add following to the `setup.cfg`:

```ini
[tool:pytest]
addopts = --cov --cov-report xml:cov.xml --cov-report term

[coverage:run]
branch = True
```

Add following to the `dangerfile.py`:

```python
import danger_py_cov

danger_py_cov.report_coverage("cov.xml", minimum_coverage=95.0)
```

Make sure to run `pytest` before running `danger-python`. 

## Development

To develop the new features, clone the repository and then run:

```sh
# install dependencies
poetry install 
# activate virtual environment
poetry shell 
# add pre-commit checks
pre-commit install -f -t pre-commit 
# run the test suite
pytest 
```

## License

`danger-py-cov` is released under an MIT license. See [LICENSE](https://github.com/elpassion/danger-py-cov/blob/master/LICENSE) for more information.
