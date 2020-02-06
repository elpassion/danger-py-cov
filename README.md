# danger-py-cov

The plugin parses the `.xml` coverage report and visualizes how the pull request affects the results. 

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

Add following to the `dangerfile.py`:

```python
import danger_py_cov

danger_py_cov.report_coverage("cov.xml", minimum_coverage=95.0)
```

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
