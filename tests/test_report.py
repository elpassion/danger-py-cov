from danger_py_cov.models import (
    CoverageFile,
    CoverageFileChangeOutput,
    DangerCoverageConfiguration,
)
from danger_py_cov.report import generate_report_for_files


def test_that_report_generates_correct_emojis():
    """
    Test that report generates correct emojis.
    """
    files = [
        CoverageFile(
            name="barely_medium.py",
            total_statements=9,
            total_branches=1,
            missed_branches=4,
            missed_statements=1,
        ),
        CoverageFile(
            name="barely_low.py",
            total_statements=15,
            total_branches=5,
            missed_statements=12,
            missed_branches=3,
        ),
        CoverageFile(
            name="barely_high.py",
            total_statements=5,
            total_branches=5,
            missed_statements=1,
            missed_branches=1,
        ),
        CoverageFile(
            name="almost_low.py",
            total_statements=10,
            total_branches=0,
            missed_statements=9,
            missed_branches=0,
        ),
    ]
    modified_files = [f.name for f in files]
    configuration = DangerCoverageConfiguration()

    output = generate_report_for_files(files, modified_files, configuration)

    assert output.total_coverage == 38.00
    assert len(output.file_changes) == 4
    assert output.file_changes[0] == CoverageFileChangeOutput(
        name="almost_low.py", coverage=10.0, emoji=":skull:"
    )
    assert output.file_changes[1] == CoverageFileChangeOutput(
        name="barely_high.py", coverage=80.0, emoji=":white_check_mark:"
    )
    assert output.file_changes[2] == CoverageFileChangeOutput(
        name="barely_low.py", coverage=25.0, emoji=":no_entry_sign:"
    )
    assert output.file_changes[3] == CoverageFileChangeOutput(
        name="barely_medium.py", coverage=50.0, emoji=":warning:"
    )
