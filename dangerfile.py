import danger_py_cov

danger_py_cov.report_coverage("cov.xml", minimum_coverage=100.0)

has_changelog = danger.git.modified_files.includes("CHANGELOG.md")

if not has_changelog:
    warn("Please add the changelog entro to CHANGELOG.md file")
