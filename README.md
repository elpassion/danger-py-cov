# danger-py-cov

The plugin parses the `.xml` coverage report and visualizes how the pull request affects the results. The report is produced  by tools such as [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.0.3/#). 

Example output:

### Current coverage is `100.00%`

| Files changed | Coverage | - |
| ------------- | -------- | --- |
| calculations.py | `100.00%` | :white_check_mark: |
| cobertura.py | `100.00%` | :white_check_mark: |
| models.py | `100.00%` | :white_check_mark: |
| plugin.py | `100.00%` | :white_check_mark: |
| report.py | `100.00%` | :white_check_mark: |

### Usage

Add following to the `dangerfile.py`:

```python
import danger_py_cov

danger_py_cov.report_coverage("cov.xml", minimum_coverage=95.0)
```
