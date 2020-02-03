from danger_python.plugins import DangerPlugin


class DangerCoverage(DangerPlugin):
    def report_coverage(self):
        self.markdown("Hello world")
