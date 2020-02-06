from .models import DangerCoverageConfiguration


def emoji_for_coverage(
    coverage: float, configuration: DangerCoverageConfiguration
) -> str:
    if coverage >= configuration.high_threshold:
        return configuration.high_emoji
    elif coverage >= configuration.medium_threshold:
        return configuration.medium_emoji
    elif coverage >= configuration.low_threshold:
        return configuration.low_emoji
    else:
        return configuration.none_emoji
