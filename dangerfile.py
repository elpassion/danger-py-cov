import danger_py_cov

danger_py_cov.report_coverage("cov.xml", minimum_coverage=100.0)

has_changelog = "CHANGELOG.md" in danger.git.modified_files

if not has_changelog:
    warn("Please add the changelog entry to CHANGELOG.md file")
